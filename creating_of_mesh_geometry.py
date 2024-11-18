import os
import numpy as np
from bgem.gmsh import gmsh
from bgem.gmsh import options as gmsh_options
from bgem.gmsh import field as gmsh_field
from bgem.stochastic import frac_plane as FP
from bgem.stochastic import frac_isec as FIC
from bgem.stochastic import fr_set
from bgem.bspline import brep_writer as bw
from bgem import Transform


# Hlavní změna je zde... muselo se smazat .set_region(fr.region)
def create_fractures_lines(gmsh_geom, fractures, base_shape: 'ObjectSet'):
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

        # Apply transformations: scale, rotate, translate
        shape = shape.scale([fr.rx, fr.ry, 0]) \
            .rotate(axis=fr.rotation_axis, angle=fr.rotation_angle) \
            .translate(fr.center)

        shapes.append(shape)

    # Fragment the fractures and return the result
    fracture_fragments = gmsh_geom.fragment(*shapes)
    return fracture_fragments


def make_mesh(parameters, fractures: fr_set.Fracture):
    # Load parameters
    mesh_file_name = parameters["output_parameters"]["mesh_file_name"]
    box_dimensions = parameters["geometry_parameters"]["box_dimensions"]
    fracture_mesh_step = parameters["geometry_parameters"]["fracture_mesh_step"]
    tolerance_initial_delaunay = parameters["mesh_parameters"]["tolerance_initial_delaunay"]
    characteristic_length_from_points = parameters["mesh_parameters"]["characteristic_length_from_points"]
    characteristic_length_from_curvature = parameters["mesh_parameters"]["characteristic_length_from_curvature"]
    characteristic_length_extend_from_boundary = parameters["mesh_parameters"][
        "characteristic_length_extend_from_boundary"]
    minimum_circle_points = parameters["mesh_parameters"]["minimum_circle_points"]
    minimum_curve_points = parameters["mesh_parameters"]["minimum_curve_points"]

    # GMSH options
    tolerance = parameters["gmsh_options_parameters"]["tolerance"]
    tolerance_boolean = parameters["gmsh_options_parameters"]["tolerance_boolean"]
    print("====================== PARAMETERS SUMMARY ======================")
    print("\nGeneral fracture information:")
    print(f"  - Number of fractures: {len(fractures)}")
    print("\nGeneral parameters:")
    print(f"  - Mesh file name: {mesh_file_name}")
    print(f"  - Box dimensions: {box_dimensions}")
    print(f"  - Fracture mesh step: {fracture_mesh_step}")
    print(f"  - Tolerance (initial Delaunay): {tolerance_initial_delaunay}")
    print(
        f"  - Characteristic length from points: {characteristic_length_from_points}")
    print(
        f"  - Characteristic length from curvature: {characteristic_length_from_curvature}")
    print(
        f"  - Characteristic length (extend from boundary): {characteristic_length_extend_from_boundary}")
    print(f"  - Minimum circle points: {minimum_circle_points}")
    print(f"  - Minimum curve points: {minimum_curve_points}")
    print(f"  - GMSH options, tolerance: {tolerance}")
    print(f"  - GMSH options, tolerance boolean: {tolerance_boolean}")

    print("\nImage parameters:")
    print(f"  - Amount of pixels: {parameters['image_parameters']['amount_of_pixels']}")
    print(f"  - Image background colour: {parameters['image_parameters']['image_background_colour']}")
    print(f"  - Colour of fractures: {parameters['image_parameters']['colour_of_fractures']}")
    print(f"  - Width of fractures: {parameters['image_parameters']['width_of_fractures']}")

    # Fracture Parameters
    print("\nFracture parameters:")
    print(f"  - Fracture box: {parameters['fracture_parameters']['fracture_box']}")
    print(f"  - Sample range: {parameters['fracture_parameters']['sample_range']}")
    print(f"  - Power: {parameters['fracture_parameters']['power']}")
    print(f"  - Confidence range: {parameters['fracture_parameters']['conf_range']}")
    print(f"  - p_32: {parameters['fracture_parameters']['p_32']}")

    # Fisher Orientation Parameters
    print("\nFisher orientation parameters:")
    print(f"  - Fisher trend: {parameters['statistics_parameters']['fisher_orientation_parameters']['fisher_trend']}")
    print(f"  - Fisher plunge: {parameters['statistics_parameters']['fisher_orientation_parameters']['fisher_plunge']}")
    print(
        f"  - Fisher concentration: {parameters['statistics_parameters']['fisher_orientation_parameters']['fisher_concentration']}")

    # Von Mises Parameters
    print("\nVon Mises parameters:")
    print(f"  - Von Mises trend: {parameters['statistics_parameters']['von_mises_parameters']['von_mises_trend']}")
    print(
        f"  - Von Mises concentration: {parameters['statistics_parameters']['von_mises_parameters']['von_mises_concentration']}")
    print("==================================================================")

    factory = gmsh.GeometryOCC(mesh_file_name, verbose=True)
    gopt = gmsh_options.Geometry()
    gopt.Tolerance = tolerance
    gopt.ToleranceBoolean = tolerance_boolean

    # Create the box geometry
    box = factory.box(box_dimensions).set_region("box")

    # Define sides of the box using the box dimensions
    side_y = factory.rectangle([box_dimensions[0], box_dimensions[1]])
    side_x = factory.rectangle([box_dimensions[1], box_dimensions[1]])

    sides = {
        "side_y0": side_y.copy().translate([0, 0, -box_dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
        "side_y1": side_y.copy().translate([0, 0, box_dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
        "side_x0": side_x.copy().translate([0, 0, -box_dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2),
        "side_x1": side_x.copy().translate([0, 0, box_dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2)
    }

    # Apply regions to each side of the box
    for name, side in sides.items():
        side.modify_regions(name)

    # Get the boundary of the box and generate fracture lines
    boundary_of_box = box.get_boundary().copy()
    fracture_fragments = create_fractures_lines(factory, fractures, factory.make_simplex(dim=1))

    # Group fractures and intersect with the box
    fractures_group = factory.group(*fracture_fragments)
    fractures_group = fractures_group.intersect(box.copy())

    # Fragment the fractures with the box
    print("Fragmenting fractures...")
    fragmented_box, fractures_fragmented = factory.fragment(box, fractures_group)
    print("Finishing geometry...")

    # Get the boundary of the fragmented box
    boundary_of_fragmented_box = fragmented_box.get_boundary()

    # Create new regions for each side of the box based on the intersection with the fragmented box
    box_all = []
    for name, side_tool in sides.items():
        isec = boundary_of_fragmented_box.select_by_intersect(side_tool)
        box_all.append(isec.modify_regions("." + name))
    box_all.extend([fragmented_box])

    # Group the fragmented fractures and intersect with the box
    boundary_fractures_group = factory.group(*fractures_fragmented.get_boundary_per_region())
    fractures_box_boundary = boundary_fractures_group.select_by_intersect(boundary_of_box).modify_regions("{}_box")
    boundary_fractures_group = factory.group(fractures_box_boundary)

    mesh_groups = [*box_all, fractures_fragmented, boundary_fractures_group]

    fractures_fragmented.mesh_step(fracture_mesh_step)

    factory.keep_only(*mesh_groups)
    factory.remove_duplicate_entities()
    factory.write_brep()

    min_element_size = fracture_mesh_step / 10
    max_element_size = np.max(box_dimensions) / 8

    mesh = gmsh_options.Mesh()
    mesh.ToleranceInitialDelaunay = tolerance_initial_delaunay
    mesh.CharacteristicLengthFromPoints = characteristic_length_from_points
    mesh.CharacteristicLengthFromCurvature = characteristic_length_from_curvature
    mesh.CharacteristicLengthExtendFromBoundary = characteristic_length_extend_from_boundary
    mesh.CharacteristicLengthMin = min_element_size
    mesh.CharacteristicLengthMax = max_element_size
    mesh.MinimumCirclePoints = minimum_circle_points
    mesh.MinimumCurvePoints = minimum_curve_points
    # factory.make_mesh(mesh_groups, dim=2)
    #factory.make_mesh(mesh_groups, dim=3)
    factory.write_mesh(format=gmsh.MeshFormat.msh2)
    os.rename(mesh_file_name + ".msh2", mesh_file_name + ".msh")
    factory.show()


# COMMENTED OUT FOR NOW
"""
def make_brep(geometry_dict, fractures: fr_set.Fracture, brep_name: str):

     Create the BREP file from a list of fractures using the brep writer interface.

    # fracture_mesh_step = geometry_dict['fracture_mesh_step']
    # dimensions = geometry_dict["box_dimensions"]

    print("n fractures:", len(fractures))

    faces = []
    for i, fr in enumerate(fractures):
        # ref_fr_points = np.array([[1.0, 1.0, 0.0], [1.0, -1.0, 0.0], [-1.0, -1.0, 0.0], [-1.0, 1.0, 0.0]]) # polovina
        ref_fr_points = fr_set.LineShape()._points
        frac_points = fr.transform(ref_fr_points)
        vtxs = [bw.Vertex(p) for p in frac_points]
        vtxs.append(vtxs[0])
        edges = [bw.Edge(a, b) for a, b in zip(vtxs[:-1], vtxs[1:])]
        face = bw.Face(edges)
        faces.append(face)

    comp = bw.Compound(faces)
    loc = Transform([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    with open(brep_name, "w") as f:
        bw.write_model(f, comp, loc)


def compute_intersections(fractures: fr_set.Fracture):
    surface = []
    fracs = []
    edges = []
    n_fr = len(fractures)

    for fracture in fractures:
        frac_plane = FP.FracPlane(fracture)
        fracs.append(frac_plane)
        surface.append(frac_plane.surface)

    p = np.array(surface).argsort()
    tolerance = 10
    for i in p:
        for j in p[i + 1:n_fr]:  # may be reduced to relevant adepts
            frac_isec = FIC.FracIsec(fractures[i], fractures[j])
            points_A, points_B = frac_isec._get_points(tolerance)
            possible_collision = FIC.FracIsec.collision_indicator(fractures[i], fractures[j], tolerance)

            if possible_collision or frac_isec.have_colision:
                print(f"collision: {frac_isec.fracture_A.id}, {frac_isec.fracture_B.id}")
            assert not possible_collision or frac_isec.have_colision

            if len(points_A) > 0:
                va1 = bw.Vertex(points_A[0, :])
                if points_A.shape[0] == 2:
                    va2 = bw.Vertex(points_A[1, :])
                    ea1 = bw.Edge(va1, va2)

            if len(points_B) > 0:
                vb1 = bw.Vertex(points_B[0, :])
                if points_B.shape[0] == 2:
                    vb2 = bw.Vertex(points_B[1, :])
                    eb1 = bw.Edge(vb1, vb2)


def check_duplicities(fi, fj, coor, vertices, tol):
    duplicity_with = -1
    duplicity_with = fi._check_duplicity(coor, tol, duplicity_with)
    duplicity_with = fj._check_duplicity(coor, tol, duplicity_with)

    for fracs in fi.isecs:
        if duplicity_with == -1:
            for ids in fracs:
                if vertices[ids].check_duplicity(coor, tol) == True:
                    duplicity_with = ids
                    break
"""
