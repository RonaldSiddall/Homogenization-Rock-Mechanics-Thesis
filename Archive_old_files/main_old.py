import GenerateMesh_old, GenerateFractures_old

parameters = {
    "fracture_parameters": {
        "sample_range": (0.038, 169),
        # SKB: Exponent škálování velikosti puklin k_r:
        # k_r je zkalibrované pro tektonické kontinuum: 2.55 až 2.79
        # k_r je zkalibrované analýzou konektivity: 2.55 až 3.45
        "k_r": 3.45,
        # SKB: Nejmenší velikost pukliny (tj. poloměr vrtu): r_min: 0.038
        # SKB: Nejvetší velikost pukliny: r_max = 169
        # => diam_range = [r_min, r_max]
        "diam_range": [0.038, 169],
        # SKB: Intenzita: p_32 [r_0, infty]: 0.59 až 2.60,
        # Intenzita: p_32, tot: 0.6 až 2.60
        "p32_r_0_to_infty": 2.5
    },
    "statistics_parameters": {
        "fisher_orientation_parameters": {
            # SKB: Trend (ve stupních): (2.5, 354.2)
            "fisher_trend": 350,
            # SKB: Plunge (ve stupních): (0.1, 85.4)
            "fisher_plunge": 80,
            # SKB: Fisherovo kappa:  (6.5, 42.9)
            "fisher_concentration": 20
        },
        "von_mises_parameters": {
            "von_mises_trend": 0,
            "von_mises_concentration": 0
        }
    },
    "geometry_parameters": {
        "rectangle_dimensions": [1, 1],
        "fracture_mesh_step": 0.01
    },
    "output_parameters": {
        "mesh_file_name": "mine_mesh"
    },
    "mesh_parameters": {
        "tolerance_initial_delaunay": 0.0001,
        "characteristic_length_from_points": True,
        "characteristic_length_from_curvature": True,
        "characteristic_length_extend_from_boundary": 2,
        "minimum_circle_points": 6,
        "minimum_curve_points": 2
    },
    "gmsh_options_parameters": {
        "tolerance": 0.0005,
        "tolerance_boolean": 0.0001
    }
}


def main_old(parameters):
    fractures_set = GenerateFractures_old.generator_of_fracture_set(parameters)
    GenerateMesh_old.make_mesh(parameters, fractures_set)


if __name__ == "__main__":
    main_old(parameters)
