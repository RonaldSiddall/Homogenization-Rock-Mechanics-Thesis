import yaml


class ConfigManager:
    def __init__(self, config_file):
        """
        Initializes the ConfigManager with the path to the configuration file
        """
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        """
        Loads the YAML configuration file into a dictionary
        """
        with open(self.config_file, "r") as file:
            config_data = yaml.safe_load(file)
        return config_data

    # Discreet fracture network (DFN) parameters
    def get_sample_range(self):
        return self.config_data["discreet_fracture_network_parameters"]["sample_range"]

    def get_k_r(self):
        return self.config_data["discreet_fracture_network_parameters"]["k_r"]

    def get_diam_range(self):
        return self.config_data["discreet_fracture_network_parameters"]["diam_range"]

    def get_p32_r_0_to_infty(self):
        return self.config_data["discreet_fracture_network_parameters"]["p32_r_0_to_infty"]

    def get_fisher_trend(self):
        return self.config_data["discreet_fracture_network_parameters"]["fisher_orientation_parameters"]["fisher_trend"]

    def get_fisher_plunge(self):
        return self.config_data["discreet_fracture_network_parameters"]["fisher_orientation_parameters"]["fisher_plunge"]

    def get_fisher_concentration(self):
        return self.config_data["discreet_fracture_network_parameters"]["fisher_orientation_parameters"]["fisher_concentration"]

    def get_von_mises_trend(self):
        return self.config_data["discreet_fracture_network_parameters"]["von_mises_parameters"]["von_mises_trend"]

    def get_von_mises_concentration(self):
        return self.config_data["discreet_fracture_network_parameters"]["von_mises_parameters"]["von_mises_concentration"]

    def get_rectangle_dimensions(self):
        return self.config_data["discreet_fracture_network_parameters"]["rectangle_dimensions"]

    # Output Parameters
    def get_mesh_file_name(self):
        return self.config_data["output_parameters"]["mesh_file_name"]

    # GMSH and mesh Parameters
    def get_tolerance_initial_delaunay(self):
        return self.config_data["gmsh_options_parameters"]["tolerance_initial_delaunay"]

    def get_fracture_mesh_step(self):
        return self.config_data["gmsh_options_parameters"]["fracture_mesh_step"]

    def get_tolerance(self):
        return self.config_data["gmsh_options_parameters"]["tolerance"]

    def get_tolerance_boolean(self):
        return self.config_data["gmsh_options_parameters"]["tolerance_boolean"]