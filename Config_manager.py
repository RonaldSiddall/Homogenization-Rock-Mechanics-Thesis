import yaml


class ConfigManager:
    def __init__(self, config_file):
        """
        Initialize the ConfigManager with the path to the configuration file.
        """
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        """
        Load the YAML configuration file into a dictionary.
        """
        with open(self.config_file, "r") as file:
            config_data = yaml.safe_load(file)
        return config_data

    # Fracture Parameters
    def get_sample_range(self):
        return self.config_data["fracture_parameters"]["sample_range"]

    def get_k_r(self):
        return self.config_data["fracture_parameters"]["k_r"]

    def get_diam_range(self):
        return self.config_data["fracture_parameters"]["diam_range"]

    def get_p32_r_0_to_infty(self):
        return self.config_data["fracture_parameters"]["p32_r_0_to_infty"]

    # Statistics Parameters
    def get_fisher_trend(self):
        return self.config_data["statistics_parameters"]["fisher_orientation_parameters"]["fisher_trend"]

    def get_fisher_plunge(self):
        return self.config_data["statistics_parameters"]["fisher_orientation_parameters"]["fisher_plunge"]

    def get_fisher_concentration(self):
        return self.config_data["statistics_parameters"]["fisher_orientation_parameters"]["fisher_concentration"]

    def get_von_mises_trend(self):
        return self.config_data["statistics_parameters"]["von_mises_parameters"]["von_mises_trend"]

    def get_von_mises_concentration(self):
        return self.config_data["statistics_parameters"]["von_mises_parameters"]["von_mises_concentration"]

    # Geometry Parameters
    def get_rectangle_dimensions(self):
        return self.config_data["geometry_parameters"]["rectangle_dimensions"]

    def get_fracture_mesh_step(self):
        return self.config_data["geometry_parameters"]["fracture_mesh_step"]

    # Output Parameters
    def get_mesh_file_name(self):
        return self.config_data["output_parameters"]["mesh_file_name"]

    # Mesh Parameters
    def get_tolerance_initial_delaunay(self):
        return self.config_data["mesh_parameters"]["tolerance_initial_delaunay"]

    def get_characteristic_length_from_points(self):
        return self.config_data["mesh_parameters"]["characteristic_length_from_points"]

    def get_characteristic_length_from_curvature(self):
        return self.config_data["mesh_parameters"]["characteristic_length_from_curvature"]

    def get_characteristic_length_extend_from_boundary(self):
        return self.config_data["mesh_parameters"]["characteristic_length_extend_from_boundary"]

    def get_minimum_circle_points(self):
        return self.config_data["mesh_parameters"]["minimum_circle_points"]

    def get_minimum_curve_points(self):
        return self.config_data["mesh_parameters"]["minimum_curve_points"]

    # GMSH Options Parameters
    def get_tolerance(self):
        return self.config_data["gmsh_options_parameters"]["tolerance"]

    def get_tolerance_boolean(self):
        return self.config_data["gmsh_options_parameters"]["tolerance_boolean"]