import os
import numpy as np
from bgem.gmsh import gmsh
from bgem.gmsh import options as gmsh_options
from bgem.gmsh import field as gmsh_field
from bgem.stochastic import frac_plane as FP
from bgem.stochastic import frac_isec as FIC
from bgem.stochastic import fr_set
from bgem.bspline import brep_writer as bw
from bgem.stochastic.fr_set import FractureSet
from bgem import Transform

# Hlavní změna je zde... muselo se smazat .set_region(fr.region)
def create_fractures_rectangles(gmsh_geom, fractures, base_shape: 'ObjectSet'):
    # From given fracture data list 'fractures',
    # transform the base_shape to fracture objects,
    # fragment fractures by their intersections,
    # and return dict: fracture.region -> GMSH object with corresponding fracture fragments.
    shapes = []

    for i, fr in enumerate(fractures):
        print("-----------------")
        print(base_shape)
        shape = base_shape.copy()
        print(shape)
        print(shape.dim_tags)
        print(shape.scale)
        print(fr)
        print("fr:", i, "tag:", shape.dim_tags)
        print("-----------------")
        shape = shape.scale([fr.rx, fr.ry, 0]).rotate(axis=fr.rotation_axis, angle=fr.rotation_angle)
        shapes.append(shape)

    fracture_fragments = gmsh_geom.fragment(*shapes)
    return fracture_fragments


def make_mesh(geometry_dict, fractures: fr_set.Fracture, mesh_name: str):
    """
    Create the GMSH mesh from a list of fractures using the bgem.gmsh interface.
    """
    fracture_mesh_step = geometry_dict['fracture_mesh_step']
    dimensions = geometry_dict["box_dimensions"]
    # well_z0, well_z1 = geometry_dict["well_opening"]
    # well_r = geometry_dict["well_effective_radius"]
    # well_dist = geometry_dict["well_distance"]

    factory = gmsh.GeometryOCC(mesh_name, verbose=True)
    gopt = gmsh_options.Geometry()
    gopt.Tolerance = 0.0001
    gopt.ToleranceBoolean = 0.001
    # gopt.MatchMeshTolerance = 1e-1

    # Main box
    box = factory.box(dimensions).set_region("box")
    # side_z = factory.rectangle([dimensions[0], dimensions[1]])
    side_y = factory.rectangle([dimensions[0], dimensions[2]])
    side_x = factory.rectangle([dimensions[2], dimensions[1]])
    # sides = dict(side_x, side_y)
    sides = dict(
        # side_z0=side_z.copy().translate([0, 0, -dimensions[2] / 2]),
        # side_z1=side_z.copy().translate([0, 0, +dimensions[2] / 2]),
        side_y0=side_y.copy().translate([0, 0, -dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
        side_y1=side_y.copy().translate([0, 0, +dimensions[1] / 2]).rotate([-1, 0, 0], np.pi / 2),
        side_x0=side_x.copy().translate([0, 0, -dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2),
        side_x1=side_x.copy().translate([0, 0, +dimensions[0] / 2]).rotate([0, 1, 0], np.pi / 2)
    )
    for name, side in sides.items():
        side.modify_regions(name)

    b_box = box.get_boundary().copy()

    # two vertical cut-off wells, just permeable part
    # left_center = [-well_dist / 2, 0, 0]
    # right_center = [+well_dist / 2, 0, 0]
    #left_well = factory.cylinder(well_r, axis=[0, 0, well_z1 - well_z0]) \
    #    .translate([0, 0, well_z0]).translate(left_center)
    # right_well = factory.cylinder(well_r, axis=[0, 0, well_z1 - well_z0]) \
    #    .translate([0, 0, well_z0]).translate(right_center)
    # b_right_well = right_well.get_boundary()
    # b_left_well = left_well.get_boundary()

    print("n fractures:", len(fractures))

    fractures = create_fractures_rectangles(factory, fractures, factory.make_simplex())
    # fractures = create_fractures_polygons(factory, fractures)
    #fractures = FractureSet.make_fractures_gmsh(gmsh_geom=factory)
    fractures_group = factory.group(*fractures)
    # fractures_group = fractures_group.remove_small_mass(fracture_mesh_step * fracture_mesh_step / 10)

    # drilled box and its boundary
    # box_drilled = box.cut(left_well, right_well)

    # fractures, fragmented, fractures boundary
    print("cut fractures by box without wells")
    fractures_group = fractures_group.intersect(box.copy())
    print("fragment fractures")
    box_fr, fractures_fr = factory.fragment(box, fractures_group)
    print("finish geometry")
    b_box_fr = box_fr.get_boundary()
    # b_left_r = b_box_fr.select_by_intersect(b_left_well).set_region(".left_well")
    # b_right_r = b_box_fr.select_by_intersect(b_right_well).set_region(".right_well")

    box_all = []
    for name, side_tool in sides.items():
        isec = b_box_fr.select_by_intersect(side_tool)
        box_all.append(isec.modify_regions("." + name))
    box_all.extend([box_fr])

    b_fractures = factory.group(*fractures_fr.get_boundary_per_region())
    b_fractures_box = b_fractures.select_by_intersect(b_box).modify_regions("{}_box")
    # b_fr_left_well = b_fractures.select_by_intersect(b_left_well).modify_regions("{}_left_well")
    # b_fr_right_well = b_fractures.select_by_intersect(b_right_well).modify_regions("{}_right_well")
    b_fractures = factory.group(b_fractures_box)
    mesh_groups = [*box_all, fractures_fr, b_fractures]

    print(fracture_mesh_step)
    # fractures_fr.set_mesh_step(fracture_mesh_step)

    factory.keep_only(*mesh_groups)
    factory.remove_duplicate_entities()
    factory.write_brep()

    min_el_size = fracture_mesh_step / 10
    fracture_el_size = np.max(dimensions) / 20
    max_el_size = np.max(dimensions) / 8

    # TOHLE JE ZAKOMENTOVANÉ, PROTOŽE field.restric je v field.py zakomentovaná metoda...

    # fracture_el_size = gmsh_field.constant(fracture_mesh_step)
    # frac_el_size_only = gmsh_field.restrict(fracture_el_size, fractures_fr, add_boundary=True)
    #gmsh_field.set_mesh_step_field(frac_el_size_only)

    mesh = gmsh_options.Mesh()
    mesh.ToleranceInitialDelaunay = 0.01
    mesh.CharacteristicLengthFromPoints = True
    mesh.CharacteristicLengthFromCurvature = True
    mesh.CharacteristicLengthExtendFromBoundary = 2
    mesh.CharacteristicLengthMin = min_el_size
    mesh.CharacteristicLengthMax = max_el_size
    mesh.MinimumCirclePoints = 6
    mesh.MinimumCurvePoints = 2

    # factory.make_mesh(mesh_groups, dim=2)
    #factory.make_mesh(mesh_groups)
    factory.write_mesh(format=gmsh.MeshFormat.msh2)
    os.rename(mesh_name + ".msh2", mesh_name + ".msh")
    factory.show()


def make_brep(geometry_dict, fractures: fr_set.Fracture, brep_name: str):
    """
    Create the BREP file from a list of fractures using the brep writer interface.
    """
    # fracture_mesh_step = geometry_dict['fracture_mesh_step']
    # dimensions = geometry_dict["box_dimensions"]

    print("n fractures:", len(fractures))

    faces = []
    for i, fr in enumerate(fractures):
        # ref_fr_points = np.array([[1.0, 1.0, 0.0], [1.0, -1.0, 0.0], [-1.0, -1.0, 0.0], [-1.0, 1.0, 0.0]]) # polovina
        ref_fr_points = fr_set.RectangleShape()._points
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

