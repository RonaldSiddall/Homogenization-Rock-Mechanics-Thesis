import os
import numpy as np
from bgem.gmsh import gmsh
from bgem.gmsh import options as gmsh_options
from bgem.stochastic import fr_set


def create_fractures_lines(factory, fractures, base_shape: 'ObjectSet'):
    """
    Create fracture objects by transforming the base shape according to each fracture's parameters,
    and fragment fractures based on their intersections with the base shape.

    Args:
    - gmsh_geom: GMSH Geometry object
    - fractures: List of Fracture objects with transformation parameters
    - base_shape: Base shape object for the fractures

    Returns:
    - fracture_fragments: Dictionary of fractures with corresponding fragments
    """
    shapes = []

    # Generate fractures by transforming the base shape
    for i, fr in enumerate(fractures):
        shape = base_shape.copy()
        print(f"Fracture index: {i}, Tag of fracture: {shape.dim_tags}")
        normal_xy = np.array([fr.normal[0], fr.normal[1], 0])
        normal_xy = normal_xy / np.linalg.norm(normal_xy)
        angle = np.arccos(np.dot(normal_xy, np.array([1, 0, 0])))
        # Apply transformations: scale, rotate, translate
        shape = shape.scale([2*fr.rx, 0, 0]) \
            .rotate(axis=np.array([0, 0, 1]), angle=angle) \
            .translate(np.array([fr.center[0], fr.center[1], 0]))
        shapes.append(shape)
    # Fragment the fractures and return the result
    fracture_fragments = factory.fragment(*shapes)
    return fracture_fragments


def make_mesh(parameters, fractures: fr_set.Fracture):
    # Load parameters
    mesh_file_name = parameters["output_parameters"]["mesh_file_name"]
    rectangle_dimensions = parameters["geometry_parameters"]["rectangle_dimensions"]
    fracture_mesh_step = parameters["geometry_parameters"]["fracture_mesh_step"]
    tolerance_initial_delaunay = parameters["mesh_parameters"]["tolerance_initial_delaunay"]
    characteristic_length_from_points = parameters["mesh_parameters"]["characteristic_length_from_points"]
    characteristic_length_from_curvature = parameters["mesh_parameters"]["characteristic_length_from_curvature"]
    characteristic_length_extend_from_boundary = parameters["mesh_parameters"]["characteristic_length_extend_from_boundary"]
    minimum_circle_points = parameters["mesh_parameters"]["minimum_circle_points"]
    minimum_curve_points = parameters["mesh_parameters"]["minimum_curve_points"]
    tolerance = parameters["gmsh_options_parameters"]["tolerance"]
    tolerance_boolean = parameters["gmsh_options_parameters"]["tolerance_boolean"]

    parameters_print_out(parameters, fractures)

    factory = gmsh.GeometryOCC(mesh_file_name, verbose=True)
    gopt = gmsh_options.Geometry()
    gopt.Tolerance = tolerance
    gopt.ToleranceBoolean = tolerance_boolean

    # Create the box geometry
    rectangle = factory.rectangle(rectangle_dimensions).set_region("rectangle")

    # Define sides of the box using the box dimensions
    side_y = factory.rectangle([rectangle_dimensions[0], rectangle_dimensions[1]])
    side_x = factory.rectangle([rectangle_dimensions[1], rectangle_dimensions[1]])

    sides = {
        "side_y0": side_y.copy().translate([0, 0, -rectangle_dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
        "side_y1": side_y.copy().translate([0, 0, rectangle_dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
        "side_x0": side_x.copy().translate([0, 0, -rectangle_dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2),
        "side_x1": side_x.copy().translate([0, 0, rectangle_dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2)
    }

    # Apply regions to each side of the box
    for name, side in sides.items():
        side.modify_regions(name)

    # Get the boundary of the box and generate fracture lines
    boundary_of_box = rectangle.get_boundary().copy()
    fracture_fragments = create_fractures_lines(factory, fractures, factory.make_simplex(dim=1))

    # Group fractures and intersect with the box
    fractures_group = factory.group(*fracture_fragments)
    fractures_group = fractures_group.intersect(rectangle.copy())

    # Fragment the fractures with the box
    print("Fragmenting fractures...")
    fragmented_rectangle, fractures_fragmented = factory.fragment(rectangle, fractures_group)
    print("Finishing geometry...")

    # Get the boundary of the fragmented box
    boundary_of_fragmented_rectangle = fragmented_rectangle.get_boundary()

    # Create new regions for each side of the rectangle based on the intersection with the fragmented rectangle
    rectangle_all = []
    for name, side_tool in sides.items():
        isec = boundary_of_fragmented_rectangle.select_by_intersect(side_tool)
        rectangle_all.append(isec.modify_regions("." + name))
    rectangle_all.extend([fragmented_rectangle])

    # Group the fragmented fractures and intersect with the box
    boundary_fractures_group = factory.group(*fractures_fragmented.get_boundary_per_region())
    fractures_box_boundary = boundary_fractures_group.select_by_intersect(boundary_of_box).modify_regions("{}_box")
    boundary_fractures_group = factory.group(fractures_box_boundary)

    mesh_groups = [*rectangle_all, fractures_fragmented, boundary_fractures_group]

    fractures_fragmented.mesh_step(fracture_mesh_step)

    factory.keep_only(*mesh_groups)
    factory.remove_duplicate_entities()
    factory.write_brep()

    min_element_size = fracture_mesh_step / 10
    max_element_size = np.max(rectangle_dimensions) / 8

    mesh = gmsh_options.Mesh()
    mesh.ToleranceInitialDelaunay = tolerance_initial_delaunay
    mesh.CharacteristicLengthFromPoints = characteristic_length_from_points
    mesh.CharacteristicLengthFromCurvature = characteristic_length_from_curvature
    mesh.CharacteristicLengthExtendFromBoundary = characteristic_length_extend_from_boundary
    mesh.CharacteristicLengthMin = min_element_size
    mesh.CharacteristicLengthMax = max_element_size
    mesh.MinimumCirclePoints = minimum_circle_points
    mesh.MinimumCurvePoints = minimum_curve_points

    factory.make_mesh(mesh_groups, dim=2)
    factory.write_mesh(format=gmsh.MeshFormat.msh2)
    os.rename(mesh_file_name + ".msh2", mesh_file_name + ".msh")
    factory.show()


def parameters_print_out(parameters, fractures):
    print("====================== PARAMETERS SUMMARY ======================")
    print("\nGeneral parameters:")
    print(f"  - Mesh file name: {parameters['output_parameters']['mesh_file_name']}.msh")
    print(f"  - Rectangle dimensions: {parameters['geometry_parameters']['rectangle_dimensions']}")
    print(f"  - Fracture mesh step: {parameters['geometry_parameters']['fracture_mesh_step']}")
    print(f"  - Tolerance (initial Delaunay): {parameters['mesh_parameters']['tolerance_initial_delaunay']}")
    print(f"  - Characteristic length from points: {parameters['mesh_parameters']['characteristic_length_from_points']}")
    print(f"  - Characteristic length from curvature: {parameters['mesh_parameters']['characteristic_length_from_curvature']}")
    print(f"  - Characteristic length (extend from boundary): {parameters['mesh_parameters']['characteristic_length_extend_from_boundary']}")
    print(f"  - Minimum circle points: {parameters['mesh_parameters']['minimum_circle_points']}")
    print(f"  - Minimum curve points: {parameters['mesh_parameters']['minimum_curve_points']}")
    print(f"  - GMSH options, tolerance: {parameters['gmsh_options_parameters']['tolerance']}")
    print(f"  - GMSH options, tolerance boolean: {parameters['gmsh_options_parameters']['tolerance_boolean']}")

    print("\nFracture parameters:")
    print(f"  - Number of fractures: {len(fractures)}")
    rectangle_dimensions = parameters['geometry_parameters']['rectangle_dimensions']
    print(f"  - Domain: {(rectangle_dimensions[0],rectangle_dimensions[1],0)}")
    print(f"  - Diam range: {parameters['fracture_parameters']['diam_range']}")
    print(f"  - Sample range: {parameters['fracture_parameters']['sample_range']}")
    print(f"  - k_r: {parameters['fracture_parameters']['k_r']}")
    print(f"  - Power: {parameters['fracture_parameters']['k_r'] - 3}")
    print(f"  - p32_r_0_to_infty: {parameters['fracture_parameters']['p32_r_0_to_infty']}")

    print("\nFisher orientation parameters:")
    print(f"  - Fisher trend: {parameters['statistics_parameters']['fisher_orientation_parameters']['fisher_trend']}")
    print(f"  - Fisher plunge: {parameters['statistics_parameters']['fisher_orientation_parameters']['fisher_plunge']}")
    print(f"  - Fisher concentration: {parameters['statistics_parameters']['fisher_orientation_parameters']['fisher_concentration']}")

    print("\nVon Mises parameters:")
    print(f"  - Von Mises trend: {parameters['statistics_parameters']['von_mises_parameters']['von_mises_trend']}")
    print(f"  - Von Mises concentration: {parameters['statistics_parameters']['von_mises_parameters']['von_mises_concentration']}")

    print("=========================== END SUMMARY ==========================")

