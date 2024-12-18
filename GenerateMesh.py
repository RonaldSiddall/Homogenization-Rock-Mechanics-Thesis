from Config_manager import ConfigManager
import os
import numpy as np
from bgem.gmsh import gmsh
from bgem.gmsh import options as gmsh_options
from bgem.stochastic.fr_set import LineShape
from bgem.gmsh import heal_mesh


class GenerateMesh:
    # Initiation of the used parameters from the config.yaml file
    def __init__(self, config_file, fracture_set):
        self.config = ConfigManager(config_file)

        # DFN parameters
        self.rectangle_dimensions = self.config.get_rectangle_dimensions()
        self.sample_range = self.config.get_sample_range()
        self.k_r = self.config.get_k_r()
        self.diam_range = self.config.get_diam_range()
        self.p32_r_0_to_infty = self.config.get_p32_r_0_to_infty()
        self.fisher_trend = self.config.get_fisher_trend()
        self.fisher_plunge = self.config.get_fisher_plunge()
        self.fisher_concentration = self.config.get_fisher_concentration()
        self.von_mises_trend = self.config.get_von_mises_trend()
        self.von_mises_concentration = self.config.get_von_mises_concentration()

        # Output
        self.mesh_file_name = self.config.get_mesh_file_name()

        # GMSH and mesh parameters
        self.tolerance_initial_delaunay = self.config.get_tolerance_initial_delaunay()
        self.tolerance = self.config.get_tolerance()
        self.tolerance_boolean = self.config.get_tolerance_boolean()
        self.fracture_mesh_step = self.config.get_fracture_mesh_step()

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
            # base shape is a basis vector that starts in XYZ origin, has length 1
            shape = base_shape.copy()
            print(f"Fracture index: {i}, Tag of fracture: {shape.dim_tags}")

            # Here the normal is not perpendicular to the fracture (it would be, if the fracture wasn't a...
            # LineShape type of fracture), but instead the normal is parallel to the Line fracture
            normal_xy = np.array([fr.normal[0], fr.normal[1], 0])

            # Normalizes the normal vector
            normal_xy = normal_xy / np.linalg.norm(normal_xy)

            # Calculates the rotation angle
            angle = np.arccos(np.dot(normal_xy, np.array([1, 0, 0])))

            # Applies transformations:
            # scale: fr.rx is the radius of the fracture, so it's multiplied by 2 to get full length of given fracture
            # rotate: projects the fracture into the XY plane
            # translate: also projects the fracture into the XY plane
            shape = shape.scale([2 * fr.rx, 0, 0]) \
                .rotate(axis=np.array([0, 0, 1]), angle=angle) \
                .translate(np.array([fr.center[0], fr.center[1], 0]))
            shapes.append(shape)

        # Fragments the fractures and returns them
        fracture_fragments = factory.fragment(*shapes)
        return fracture_fragments

    def make_mesh(self):
        """
        This method generates the geometry and mesh for the fractured domain using GMSH
        """
        factory = gmsh.GeometryOCC(self.mesh_file_name, verbose=True)
        gopt = gmsh_options.Geometry()
        gopt.Tolerance = self.tolerance
        gopt.ToleranceBoolean = self.tolerance_boolean

        # Creates the rectangle geometry
        rectangle = factory.rectangle(self.rectangle_dimensions).set_region("rock")

        # Defines the sides of the rectangle using the rectangle dimensions
        side_y = factory.rectangle([self.rectangle_dimensions[0], self.rectangle_dimensions[1]])
        side_x = factory.rectangle([self.rectangle_dimensions[1], self.rectangle_dimensions[1]])

        sides = {
            "side_y0": side_y.copy().translate([0, 0, -self.rectangle_dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
            "side_y1": side_y.copy().translate([0, 0, self.rectangle_dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
            "side_x0": side_x.copy().translate([0, 0, -self.rectangle_dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2),
            "side_x1": side_x.copy().translate([0, 0, self.rectangle_dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2)
        }

        # Creates regions for each side of the rectangle
        for name, side in sides.items():
            side.modify_regions(name)

        # This is the region (physical group), that defines the domain ie the rectangle
        boundary_of_rectangle = rectangle.get_boundary().copy()

        # Generates fractures that are fragmented
        fracture_fragments = self.create_fractures_lines(factory, LineShape.gmsh_base_shape(self, factory))

        # This groups the fractures into a physical group, including the points that are the intersections
        # of the fractures and the boundary
        fractures_group = factory.group(*fracture_fragments).set_region("fractures")
        fractures_group = fractures_group.intersect(rectangle.copy())

        # Fragments the fractures with the rectangle
        print("Fragmenting fractures...")
        fragmented_rectangle, fractures_fragmented = factory.fragment(rectangle, fractures_group)

        # Gets the boundary of the fragmented rectangle
        boundary_of_fragmented_rectangle = fragmented_rectangle.get_boundary()

        # This for cycle creates 4 regions (physical groups), each of these groups not only contains the side of
        # the rectangle, but also the points of intersecting fractures with the boundary
        rectangle_all = []
        for name, side_tool in sides.items():
            intersections = boundary_of_fragmented_rectangle.select_by_intersect(side_tool)
            rectangle_all.append(intersections.modify_regions("." + name))
        rectangle_all.extend([fragmented_rectangle])

        # This group contains all points within domain (including intersections between fractures and fractures
        # with boundary), only 4 points are not included - the vertices of the domain (square)
        boundary_fractures_group = factory.group(*fractures_fragmented.get_boundary_per_region())

        # This contains all the intersecting points between the fractures and the whole boundary (all 4 sides)
        # Does not include the 4 points in the vertices of the domain
        fractures_rectangle_boundary = boundary_fractures_group.select_by_intersect(boundary_of_rectangle)

        # This groups all the fractures that are on the boundary of the rectangle
        boundary_fractures_group = factory.group(fractures_rectangle_boundary)

        # In this for cycle 4 regions (physical groups) are made. Each contains the points of intersecting fractures
        # and boundary that are on that given side of the rectangle
        sides_fractures = []
        for name, side in sides.items():
            side_fractures = fractures_rectangle_boundary.select_by_intersect(sides[f"{name}"]).set_region(
                f".{name}_fractures")
            sides_fractures.append(side_fractures)

        print("Finishing geometry...")

        # Defines mesh groups that are used in meshing
        mesh_groups = [*rectangle_all, fractures_fragmented, *sides_fractures]

        # Sets the mesh step for the fragmented fractures
        fractures_fragmented.mesh_step(self.fracture_mesh_step)

        # Finalizes the mesh and removes any duplicate entities
        factory.keep_only(*mesh_groups)
        factory.remove_duplicate_entities()

        # Sets the mesh element size
        min_element_size = self.fracture_mesh_step / 10
        max_element_size = np.max(self.rectangle_dimensions) / 8

        # Sets mesh options
        mesh = gmsh_options.Mesh()

        # These are the pre-set options
        mesh.CharacteristicLengthFromPoints = True
        mesh.CharacteristicLengthFromCurvature = True
        mesh.CharacteristicLengthExtendFromBoundary = 2
        mesh.MinimumCirclePoints = 6
        mesh.MinimumCurvePoints = 2

        # These parameters can be changed by the user
        mesh.ToleranceInitialDelaunay = self.tolerance_initial_delaunay
        mesh.CharacteristicLengthMin = min_element_size
        mesh.CharacteristicLengthMax = max_element_size

        # Creates the 2D mesh and saves it in the required format for FLOW123D
        factory.make_mesh(mesh_groups, dim=2)
        factory.write_mesh(format=gmsh.MeshFormat.msh)

        # Method that prints the parameter summary
        self.parameters_info_print_out()
        factory.show()

        # These lines heal the created .msh file, so that it can be simulated
        hm = heal_mesh.HealMesh.read_mesh(self.mesh_file_name + ".msh")
        hm.heal_mesh(gamma_tol=0.01)
        hm.write(self.mesh_file_name + "_healed.msh")

    def parameters_info_print_out(self):
        print("====================== PARAMETERS SUMMARY ======================")
        print("\nGeneral parameters:")
        print(f"  - Mesh file name: {self.mesh_file_name}.msh")
        print(f"  - Rectangle dimensions: {self.rectangle_dimensions}")
        print(f"  - Fracture mesh step: {self.fracture_mesh_step}")
        print(f"  - Tolerance (initial Delaunay): {self.tolerance_initial_delaunay}")
        print(f"  - GMSH options, tolerance: {self.tolerance}")
        print(f"  - GMSH options, tolerance boolean: {self.tolerance_boolean}")

        print("\nFracture parameters:")
        print(f"  - Number of fractures: {len(self.fracture_set)}")
        print(f"  - domain: {(self.rectangle_dimensions[0], self.rectangle_dimensions[1], 0)}")
        print(f"  - Diam range: {self.diam_range}")
        print(f"  - Sample range: {self.sample_range}")
        print(f"  - k_r: {self.k_r}")
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
