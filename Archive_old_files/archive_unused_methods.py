# =========================================
# BACKUP FOR IMAGE PLOTTING
# =========================================
"""
from PIL import Image, ImageDraw

def scale_cut(x, s):
    # Scales and cuts the coordinates based on the defined width and height.
    return tuple([max(0, min(sv, int(sv * xv))) for xv, sv in zip(x[:2], s)])


def plotting_of_dfn(parameters, fractures):
    amount_of_pixels = parameters["image_parameters"]["amount_of_pixels"]
    image_background_colour = parameters["image_parameters"]["image_background_colour"]
    colour_of_fractures = parameters["image_parameters"]["colour_of_fractures"]
    width_of_fractures = parameters["image_parameters"]["width_of_fractures"]

    image = Image.new('RGBA', amount_of_pixels, image_background_colour)
    draw = ImageDraw.Draw(image)
    for fr in fractures:
        # it used to be t = 0.5 * fr.r * np.array([-fr.normal[2], fr.normal[1], 0]),
        # but I would get vertical lines only, I guess because of the z component being zero
        t = 0.5 * fr.r * np.array([-fr.normal[1], fr.normal[0], 0])
        a = scale_cut(0.5 + fr.center - t, amount_of_pixels)
        b = scale_cut(0.5 + fr.center + t, amount_of_pixels)
        draw.line((a, b), fill=colour_of_fractures, width=width_of_fractures)
    image.show()

def compute_p32_r_min_to_r_max(parameters):
    # computes and returns p_32[r_min, r_max], p_32
    p32_r_0_to_infty = parameters["fracture_parameters"]["p32_r_0_to_infty"]
    diam_range = parameters["fracture_parameters"]["diam_range"]
    r_0 = diam_range[0]
    sample_range = parameters["fracture_parameters"]["sample_range"]
    r_min = sample_range[0]
    r_max = sample_range[1]
    k_r = parameters["fracture_parameters"]["k_r"]
    p32_r_min_to_r_max = p32_r_0_to_infty*(((r_min)**(2-k_r)-(r_max)**(2-k_r))/(r_0**(2-k_r)))

    return p32_r_min_to_r_max
"""
# =========================================
# BACKUP FOR BREP,
# =========================================
from bgem.gmsh import field as gmsh_field
from bgem.stochastic import frac_plane as FP
from bgem.stochastic import frac_isec as FIC
from bgem.bspline import brep_writer as bw
from bgem import Transform

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