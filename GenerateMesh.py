from Config_manager import ConfigManager
import os
import numpy as np
from bgem.gmsh import gmsh
from bgem.gmsh import options as gmsh_options


class GenerateMesh:
    # Initiation of the used parameters from the config.yaml file
    def __init__(self, config_file, fracture_set):
        self.config = ConfigManager(config_file)

        # Fracture parameters
        self.sample_range = self.config.get_sample_range()
        self.k_r = self.config.get_k_r()
        self.diam_range = self.config.get_diam_range()
        self.p32_r_0_to_infty = self.config.get_p32_r_0_to_infty()

        # Statistics parameters
        self.fisher_trend = self.config.get_fisher_trend()
        self.fisher_plunge = self.config.get_fisher_plunge()
        self.fisher_concentration = self.config.get_fisher_concentration()
        self.von_mises_trend = self.config.get_von_mises_trend()
        self.von_mises_concentration = self.config.get_von_mises_concentration()

        # Geometry Parameters
        self.fracture_mesh_step = self.config.get_fracture_mesh_step()
        self.rectangle_dimensions = self.config.get_rectangle_dimensions()

        # Output
        self.mesh_file_name = self.config.get_mesh_file_name()

        # Mesh parameters
        self.tolerance_initial_delaunay = self.config.get_tolerance_initial_delaunay()
        self.characteristic_length_from_points = self.config.get_characteristic_length_from_points()
        self.characteristic_length_from_curvature = self.config.get_characteristic_length_from_curvature()
        self.characteristic_length_extend_from_boundary = self.config.get_characteristic_length_extend_from_boundary()
        self.minimum_circle_points = self.config.get_minimum_circle_points()
        self.minimum_curve_points = self.config.get_minimum_curve_points()

        # GMSH options parameters
        self.tolerance = self.config.get_tolerance()
        self.tolerance_boolean = self.config.get_tolerance_boolean()

        # FractureSet that contains all the Fracture objects from the GenerateFractures class
        self.fracture_set = fracture_set

    def create_fractures_lines(self, factory, base_shape: 'ObjectSet'):
        """
        This method creates fracture objects by transforming the base shape according to each of the
        fracture's parameters, then fragments the fractures based on their intersections with the base shape
        """
        shapes = []

        # Generates fractures by transforming the base shape
        for i, fr in enumerate(self.fracture_set):
            shape = base_shape.copy()
            print(f"Fracture index: {i}, Tag of fracture: {shape.dim_tags}")
            # Here the normal is not perpendicular to the fracture (it would be, if the fracture wasn't a...
            # LineShape type of fracture), but instead the normal is parallel to the Line fracture
            normal_xy = np.array([fr.normal[0], fr.normal[1], 0])
            # Normalize the normal vector
            normal_xy = normal_xy / np.linalg.norm(normal_xy)
            # Calculate the rotation angle
            angle = np.arccos(np.dot(normal_xy, np.array([1, 0, 0])))

            # Apply transformations: scale, rotate, translate
            shape = shape.scale([2 * fr.rx, 0, 0]) \
                .rotate(axis=np.array([0, 0, 1]), angle=angle) \
                .translate(np.array([fr.center[0], fr.center[1], 0]))
            shapes.append(shape)

        # Fragments the fractures and returns the result
        fracture_fragments = factory.fragment(*shapes)
        return fracture_fragments

    def make_mesh(self):
        """
        This method generates the mesh for the fractured domain using GMSH
        """
        factory = gmsh.GeometryOCC(self.mesh_file_name, verbose=True)  # Create a GMSH geometry factory
        gopt = gmsh_options.Geometry()  # GMSH geometry options
        gopt.Tolerance = self.tolerance
        gopt.ToleranceBoolean = self.tolerance_boolean

        # Method that prints the parameter summary
        self.parameters_info_print_out()

        # Creates the rectangle geometry
        rectangle = factory.rectangle(self.rectangle_dimensions).set_region("rectangle")

        # Defines the sides of the rectangle using the rectangle dimensions
        side_y = factory.rectangle([self.rectangle_dimensions[0], self.rectangle_dimensions[1]])
        side_x = factory.rectangle([self.rectangle_dimensions[1], self.rectangle_dimensions[1]])

        sides = {
            "side_y0": side_y.copy().translate([0, 0, -self.rectangle_dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
            "side_y1": side_y.copy().translate([0, 0, self.rectangle_dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
            "side_x0": side_x.copy().translate([0, 0, -self.rectangle_dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2),
            "side_x1": side_x.copy().translate([0, 0, self.rectangle_dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2)
        }

        # Applies regions to each side of the box
        for name, side in sides.items():
            side.modify_regions(name)

        # Get the boundary of the box and generate fracture lines
        boundary_of_box = rectangle.get_boundary().copy()
        fracture_fragments = self.create_fractures_lines(factory, factory.make_simplex(dim=1))

        # Groups the fractures and intersects with the box
        fractures_group = factory.group(*fracture_fragments)
        fractures_group = fractures_group.intersect(rectangle.copy())

        # Fragments the fractures with the rectangle
        print("Fragmenting fractures...")
        fragmented_rectangle, fractures_fragmented = factory.fragment(rectangle, fractures_group)
        print("Finishing geometry...")

        # Gets the boundary of the fragmented rectangle
        boundary_of_fragmented_rectangle = fragmented_rectangle.get_boundary()

        # Creates new regions for each side of the rectangle based on the intersection with the fragmented rectangle
        rectangle_all = []
        for name, side_tool in sides.items():
            isec = boundary_of_fragmented_rectangle.select_by_intersect(side_tool)
            rectangle_all.append(isec.modify_regions("." + name))
        rectangle_all.extend([fragmented_rectangle])

        # Groups the fragmented fractures and intersects with the box
        boundary_fractures_group = factory.group(*fractures_fragmented.get_boundary_per_region())
        fractures_box_boundary = boundary_fractures_group.select_by_intersect(boundary_of_box).modify_regions("{}_box")
        boundary_fractures_group = factory.group(fractures_box_boundary)

        # Defines mesh groups
        mesh_groups = [*rectangle_all, fractures_fragmented, boundary_fractures_group]

        # Sets mesh step for the fragmented fractures
        fractures_fragmented.mesh_step(self.fracture_mesh_step)

        # Finalizes the mesh and removes any duplicate entities
        factory.keep_only(*mesh_groups)
        factory.remove_duplicate_entities()
        factory.write_brep()

        # Set the mesh element size
        min_element_size = self.fracture_mesh_step / 10
        max_element_size = np.max(self.rectangle_dimensions) / 8

        # Sets mesh options
        mesh = gmsh_options.Mesh()
        mesh.ToleranceInitialDelaunay = self.tolerance_initial_delaunay
        mesh.CharacteristicLengthFromPoints = self.characteristic_length_from_points
        mesh.CharacteristicLengthFromCurvature = self.characteristic_length_from_curvature
        mesh.CharacteristicLengthExtendFromBoundary = self.characteristic_length_extend_from_boundary
        mesh.CharacteristicLengthMin = min_element_size
        mesh.CharacteristicLengthMax = max_element_size
        mesh.MinimumCirclePoints = self.minimum_circle_points
        mesh.MinimumCurvePoints = self.minimum_curve_points

        # Creates the mesh and saves it in the required format for FLOW123D
        factory.make_mesh(mesh_groups, dim=2)
        factory.write_mesh(format=gmsh.MeshFormat.msh2)
        os.rename(self.mesh_file_name + ".msh2", self.mesh_file_name + ".msh")
        factory.show()

    def parameters_info_print_out(self):
        print("====================== PARAMETERS SUMMARY ======================")
        print("\nGeneral parameters:")
        print(f"  - Mesh file name: {self.mesh_file_name}.msh")
        print(f"  - Rectangle dimensions: {self.rectangle_dimensions}")
        print(f"  - Fracture mesh step: {self.fracture_mesh_step}")
        print(f"  - Tolerance (initial Delaunay): {self.tolerance_initial_delaunay}")
        print(f"  - Characteristic length from points: {self.characteristic_length_from_points}")
        print(f"  - Characteristic length from curvature: {self.characteristic_length_from_curvature}")
        print(f"  - Characteristic length (extend from boundary): {self.characteristic_length_extend_from_boundary}")
        print(f"  - Minimum circle points: {self.minimum_circle_points}")
        print(f"  - Minimum curve points: {self.minimum_curve_points}")
        print(f"  - GMSH options, tolerance: {self.tolerance}")
        print(f"  - GMSH options, tolerance boolean: {self.tolerance_boolean}")

        print("\nFracture parameters:")
        print(f"  - Number of fractures: {len(self.fracture_set)}")
        print(f"  - domain: {(self.rectangle_dimensions[0], self.rectangle_dimensions[1], 0)}")
        print(f"  - Diam range: {self.diam_range}")
        print(f"  - Sample range: {self.sample_range}")
        print(f"  - k_r: {self.k_r}")
        print(f"  - power: {self.k_r - 3}")
        print(f"  - p32_r_0_to_infty: {self.p32_r_0_to_infty}")
        print("\nFisher orientation parameters:")
        print(f"  - Fisher trend: {self.fisher_trend}")
        print(f"  - Fisher plunge: {self.fisher_plunge}")
        print(
            f"  - Fisher concentration: {self.fisher_concentration}")
        print("\nVon Mises parameters:")
        print(f"  - Von Mises trend: {self.von_mises_trend}")
        print(
            f"  - Von Mises concentration: {self.von_mises_concentration}")
        print("==================================================================")
