import generator_of_fractures_and_plotting
import creating_of_mesh_geometry
from bgem.stochastic.fr_set import FractureSet

parameters = {
    "image_parameters": {
        "amount_of_pixels": (1000, 1000),
        "image_background_colour": (255, 255, 255, 255),
        "colour_of_fractures": (0, 0, 0),
        "width_of_fractures": 1
    },
    "fracture_parameters": {
        "fracture_box": [1, 1, 0],
        "sample_range": (0.001, 1),
        "power": 2.1,
        "conf_range": [0.001, 1],
        "p_32": 3.1
    },
    "statistics_parameters": {
        "fisher_orientation_parameters": {
            "fisher_trend": 0,
            "fisher_plunge": 90,
            "fisher_concentration": 0
        },
        "von_mises_parameters": {
            "von_mises_trend": 0,
            "von_mises_concentration": 0
        }
    },
    "geometry_parameters": {
        "box_dimensions": [1, 1, 1],
        "fracture_mesh_step": 1
    },
    "output_parameters": {
        "mesh_file_name": "mine_mesh"
    },
    "mesh_parameters": {
        "tolerance_initial_delaunay": 0.01,
        "characteristic_length_from_points": True,
        "characteristic_length_from_curvature": True,
        "characteristic_length_extend_from_boundary": 2,
        "minimum_circle_points": 6,
        "minimum_curve_points": 2
    },
    "gmsh_options_parameters": {
        "tolerance": 0.0001,
        "tolerance_boolean": 0.001
    }
}


def main(parameters):
    fractures_list = generator_of_fractures_and_plotting.fractures_generation(parameters)
    fractures = FractureSet.from_list(fractures_list)
    creating_of_mesh_geometry.make_mesh(parameters, fractures)


if __name__ == "__main__":
    main(parameters)
