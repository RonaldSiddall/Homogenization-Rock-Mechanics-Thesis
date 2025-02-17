import os
import ruamel.yaml
yaml = ruamel.yaml.YAML()
from check_values_in_config_file import check_values_in_config_file_yaml
from path_manager import get_all_needed_paths_yaml
from ConfigManager import ConfigManager

class GenerateYaml:
    # Initiation of the used parameters from the config.yaml file
    def __init__(self, config_file, mesh_file):
        # This checks the values within the config file
        control_variable = check_values_in_config_file_yaml(config_file)
        if control_variable is False:
            return  # Skips everything if validation failed

        # Loading of the config_file
        self.config = ConfigManager(config_file)
        needed_paths = get_all_needed_paths_yaml(config_file, mesh_file)

        self.config_file = needed_paths[0]
        self.mesh_file = needed_paths[1]
        self.path_to_yaml_template = needed_paths[2]
        self.yaml_output_dir = needed_paths[3].replace("/C", "C:")  # Directory where the YAML will be saved
        self.rectangle_dimensions = self.config.get_rectangle_dimensions()
        self.change_names_of_computed_yaml = self.config.get_change_names_of_computed_yaml()
        self.new_name_of_yaml = self.config.get_new_name_of_yaml()

        # Homogenization settings
        self.cross_section_multiplier = self.config.get_cross_section_multiplier()
        self.young_modul_rock_gpa = self.config.get_young_modul_rock_gpa()
        self.reduction_value_for_fractures = self.config.get_reduction_value_for_fractures()

        # Optional settings
        self.create_complete_summary_txt_file_yaml = self.config.get_create_complete_summary_txt_file_yaml()
        self.dir_of_where_summary_is_created_yaml = needed_paths[4]

    def generate_yaml(self):
        # Extract the first and second value of rectangle_dimensions that are used in config_file.yaml
        rectangle_first_dimension = self.rectangle_dimensions[0]
        rectangle_second_dimension = self.rectangle_dimensions[1]
        new_cross_section = self.cross_section_multiplier * rectangle_first_dimension * rectangle_second_dimension

        # We need the Young modulus to be in Pascals
        young_modul_rock_pa = 1000 * self.young_modul_rock_gpa

        reduced_young_modul_fractures = young_modul_rock_pa / self.reduction_value_for_fractures

        # Read the simulation.yaml file
        with open(self.path_to_yaml_template, "r") as template_file:
            template_data = yaml.load(template_file)
            template_data["problem"]["mesh"]["mesh_file"] = self.mesh_file
            template_data["problem"]["flow_equation"]["flow_equation"]["input_fields"][0]["cross_section"] = new_cross_section
            template_data["problem"]["flow_equation"]["mechanics_equation"]["input_fields"][0]["young_modulus"] = young_modul_rock_pa
            template_data["problem"]["flow_equation"]["mechanics_equation"]["input_fields"][1]["young_modulus"] = reduced_young_modul_fractures

        # Save the modified simulation.yaml
        with open(self.yaml_output_dir, "w") as created_yaml_file:
            yaml.dump(template_data, created_yaml_file)