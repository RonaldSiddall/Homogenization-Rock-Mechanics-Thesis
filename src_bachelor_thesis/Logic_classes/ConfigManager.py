import os
import yaml

class ConfigManager:
    # Initializes the ConfigManager with the path to the configuration file
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_config()

    # Loads the YAML configuration file into a dictionary
    def load_config(self):
        with open(self.config_file, "r") as file:
            config_data = yaml.safe_load(file)
        return config_data

    # This absolute path is CRUCIAL, because literally every other directory is derived from this one
    def get_absolute_path_to_dir_with_project(self):
        return self.config_data["absolute_path_to_project"]

    # This part underneath is related to the script create_mesh.py that creates .msh (and also _healed.msh) file
    ############################################################################################################################
    # Output settings
    def get_dir_where_mesh_is_created(self):
        dir_where_mesh_is_created = self.get_absolute_path_to_dir_with_project() + self.config_data["mesh_and_fracture_network_settings"]["output"]["dir_where_mesh_is_created"]
        os.makedirs(dir_where_mesh_is_created, exist_ok=True)
        return dir_where_mesh_is_created
    def get_customize_mesh_name(self):
        return self.config_data["mesh_and_fracture_network_settings"]["output"]["customize_mesh_name"]
    def get_new_mesh_file_name(self):
        return self.config_data["mesh_and_fracture_network_settings"]["output"]["new_mesh_file_name"]

    # Discreet fracture network (DFN) parameters
    def get_sample_range(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["sample_range"]
    def get_k_r(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["k_r"]
    def get_diam_range(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["diam_range"]
    def get_p32_r0_to_r_infty(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["p32_r0_to_r_infty"]
    def get_fisher_trend(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["fisher_orientation_parameters"]["fisher_trend"]
    def get_fisher_plunge(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["fisher_orientation_parameters"]["fisher_plunge"]
    def get_fisher_kappa(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["fisher_orientation_parameters"]["fisher_kappa"]
    def get_von_mises_trend(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["von_mises_parameters"]["von_mises_trend"]
    def get_von_mises_kappa(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["von_mises_parameters"]["von_mises_kappa"]
    def get_rectangle_dimensions(self):
        return self.config_data["mesh_and_fracture_network_settings"]["discreet_fracture_network_parameters"]["rectangle_dimensions"]

    # GMSH and mesh Parameters
    def get_tolerance_initial_delaunay(self):
        return self.config_data["mesh_and_fracture_network_settings"]["gmsh_options_parameters"]["tolerance_initial_delaunay"]
    def get_fracture_mesh_step(self):
        return self.config_data["mesh_and_fracture_network_settings"]["gmsh_options_parameters"]["fracture_mesh_step"]
    def get_tolerance(self):
        return self.config_data["mesh_and_fracture_network_settings"]["gmsh_options_parameters"]["tolerance"]
    def get_tolerance_boolean(self):
        return self.config_data["mesh_and_fracture_network_settings"]["gmsh_options_parameters"]["tolerance_boolean"]

    # Optional settings
    def get_display_fracture_network(self):
        return self.config_data["mesh_and_fracture_network_settings"]["optional_settings"]["display_fracture_network"]
    def get_create_complete_summary_txt_file_mesh(self):
        return self.config_data["mesh_and_fracture_network_settings"]["optional_settings"]["create_complete_summary_txt_file_mesh"]
    def get_dir_of_where_summary_is_created_mesh(self):
        dir_of_where_summary_is_created_mesh = self.get_absolute_path_to_dir_with_project() + self.config_data["mesh_and_fracture_network_settings"]["optional_settings"]["dir_of_where_summary_is_created_mesh"]
        os.makedirs(dir_of_where_summary_is_created_mesh, exist_ok=True)
        return dir_of_where_summary_is_created_mesh
    def get_change_name_of_txt_file_summary_mesh(self):
        return self.config_data["mesh_and_fracture_network_settings"]["optional_settings"]["change_name_of_txt_file_summary_mesh"]
    def get_new_txt_file_summary_name_mesh(self):
        return self.config_data["mesh_and_fracture_network_settings"]["optional_settings"]["new_txt_file_summary_name_mesh"]
    # End of the part related to the script create_mesh.py
    ############################################################################################################################


    # This part underneath is related to the script create_yaml.py that creates .yaml file
    ############################################################################################################################
    # Input settings
    def get_boundary_conditions_have_equal_displacement(self):
        return self.config_data["homogenization_and_yaml_creation"]["input"]["boundary_conditions_have_equal_displacement"]

    def get_displacement_percentage_all_boundary_conditions(self):
        return self.config_data["homogenization_and_yaml_creation"]["input"]["displacement_percentage_all_boundary_conditions"]

    def get_displacement_percentage_x(self):
        return self.config_data["homogenization_and_yaml_creation"]["input"]["displacement_percentage_x"]

    def get_displacement_percentage_y(self):
        return self.config_data["homogenization_and_yaml_creation"]["input"]["displacement_percentage_y"]

    def get_displacement_percentage_shear(self):
        return self.config_data["homogenization_and_yaml_creation"]["input"]["displacement_percentage_shear"]
    # Output settings
    def get_path_to_yaml_template(self):
        return self.get_absolute_path_to_dir_with_project() + self.config_data["homogenization_and_yaml_creation"]["output"]["path_to_yaml_template"]

    def get_dir_where_yaml_is_created(self):
        absolute_path = self.get_absolute_path_to_dir_with_project().replace("C:", "/C")
        return absolute_path + self.config_data["homogenization_and_yaml_creation"]["output"]["dir_where_yaml_is_created"]

    def get_change_names_of_computed_yaml(self):
        return self.config_data["homogenization_and_yaml_creation"]["output"]["change_names_of_computed_yaml"]

    def get_new_name_of_yaml(self):
        return self.config_data["homogenization_and_yaml_creation"]["output"]["new_name_of_yaml"]

    # Homogenization_settings
    def get_cross_section_multiplier(self):
        return self.config_data["homogenization_and_yaml_creation"]["homogenization_settings"]["cross_section_multiplier"]

    def get_young_modul_rock_gpa(self):
        return self.config_data["homogenization_and_yaml_creation"]["homogenization_settings"]["young_modul_rock_gpa"]

    def get_reduction_value_for_fractures(self):
        return self.config_data["homogenization_and_yaml_creation"]["homogenization_settings"]["reduction_value_for_fractures"]

    # Optional settings
    def get_create_complete_summary_txt_file_yaml(self):
        return self.config_data["homogenization_and_yaml_creation"]["optional_settings"]["create_complete_summary_txt_file_yaml"]

    def get_dir_of_where_summary_is_created_yaml(self):
        dir_of_where_summary_is_created_yaml = self.get_absolute_path_to_dir_with_project() + self.config_data["homogenization_and_yaml_creation"]["optional_settings"]["dir_of_where_summary_is_created_yaml"]
        if self.get_create_complete_summary_txt_file_yaml() == "yes":
            os.makedirs(dir_of_where_summary_is_created_yaml, exist_ok=True)
        return dir_of_where_summary_is_created_yaml

    def get_change_name_of_txt_file_summary_yaml(self):
        return self.config_data["homogenization_and_yaml_creation"]["optional_settings"]["change_name_of_txt_file_summary_yaml"]

    def get_new_txt_file_summary_name_yaml(self):
        return self.config_data["homogenization_and_yaml_creation"]["optional_settings"]["new_txt_file_summary_name_yaml"]
    # End of the part related to the script create_mesh.py
    ############################################################################################################################

    # This part underneath is related to the script create_tensor.py that outputs .txt file with final tensor
    ############################################################################################################################
    # Important: It is expected that the path to the .bat script that runs the simulation will not be changed
    # However if the user wants to change this path it can be done by rewriting the command below
    def get_path_to_flow123d_script(self):
        return self.get_absolute_path_to_dir_with_project() + "src_bachelor_thesis/Utility_methods/flow-noterm.bat"

    # Output settings
    def get_name_of_file_with_tensor(self):
        return self.config_data["simulation_and_final_tensor_computation_settings"]["output"]["name_of_file_with_tensor"]

    def get_output_dir_of_simulation_results(self):
        output_dir_of_simulation_results = self.get_absolute_path_to_dir_with_project() + self.config_data["simulation_and_final_tensor_computation_settings"]["output"]["output_dir_of_simulation_results"]
        os.makedirs(output_dir_of_simulation_results, exist_ok=True)
        output_dir_of_simulation_results = output_dir_of_simulation_results.replace("C:", "/C")
        return output_dir_of_simulation_results

    def get_output_dir_of_file_with_tensor(self):
        output_dir_of_file_with_tensor = self.get_absolute_path_to_dir_with_project() + self.config_data["simulation_and_final_tensor_computation_settings"]["output"]["output_dir_of_file_with_tensor"]
        os.makedirs(output_dir_of_file_with_tensor, exist_ok=True)
        output_dir_of_file_with_tensor = output_dir_of_file_with_tensor + self.get_name_of_file_with_tensor()
        return output_dir_of_file_with_tensor

    # Optional settings
    def get_display_std_output(self):
        return self.config_data["simulation_and_final_tensor_computation_settings"]["optional_settings"]["display_std_output"]
    # End of the part related to the script create_tensor.py
    ############################################################################################################################