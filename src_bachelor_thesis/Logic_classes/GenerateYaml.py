import ruamel.yaml
yaml = ruamel.yaml.YAML()
from Utility_methods.check_values_in_config_file import check_values_in_config_file_yaml
from Utility_methods.path_manager import get_all_needed_paths_yaml
from Logic_classes.ConfigManager import ConfigManager

class GenerateYaml:
    # Initiation of the used parameters from the config.yaml file
    def __init__(self, config_file, mesh_file):
        # This checks the values within the config file
        control_variable = check_values_in_config_file_yaml(config_file)
        if control_variable is False:
            return  # Skips everything if validation failed

        # Loading of needed parameters from the config_file or needed paths
        self.config = ConfigManager(config_file)
        self.rectangle_dimensions = self.config.get_rectangle_dimensions()

        needed_paths_yaml = get_all_needed_paths_yaml(config_file, mesh_file)
        self.mesh_file = needed_paths_yaml[1]
        self.path_to_yaml_template = needed_paths_yaml[2]
        self.yaml_output_dir = needed_paths_yaml[3].replace("/C", "C:")

        # Homogenization settings
        self.cross_section_multiplier = self.config.get_cross_section_multiplier()
        self.young_modul_rock_gpa = self.config.get_young_modul_rock_gpa()
        self.reduction_value_for_fractures = self.config.get_reduction_value_for_fractures()
        self.boundary_conditions_have_equal_displacement = self.config.get_boundary_conditions_have_equal_displacement()
        self.displacement_percentage_all_boundary_conditions = self.config.get_displacement_percentage_all_boundary_conditions()
        self.displacement_percentage_x = self.config.get_displacement_percentage_x()
        self.displacement_percentage_y = self.config.get_displacement_percentage_y()
        self.displacement_percentage_z = self.config.get_displacement_percentage_shear()

    def generate_yaml(self):
        # Extracts the first and second value of rectangle_dimensions that are used in config_file.yaml
        rectangle_first_dimension = self.rectangle_dimensions[0]
        rectangle_second_dimension = self.rectangle_dimensions[1]

        # Computes the new cross-section for the fractures
        new_cross_section_of_fractures = self.cross_section_multiplier * rectangle_first_dimension * rectangle_second_dimension

        # We need the Young modulus of rock to be in Pascals instead of giga Pascals
        young_modul_rock_pa = 1000 * self.young_modul_rock_gpa

        reduced_young_modul_fractures = young_modul_rock_pa / self.reduction_value_for_fractures

        # Old words represent the keywords that are replaced in the yaml template with the values given by config data
        old_words = ["displacement_percentage_x", "displacement_percentage_y", "displacement_percentage_shear",
                     "output_mesh_path", "fractures_cross_section", "rock_young_modulus", "fractures_young_modulus"]

        # New words replace the old words with the needed value, depending on if displacements are equal or not
        if self.boundary_conditions_have_equal_displacement == "yes":
            new_words = [self.displacement_percentage_all_boundary_conditions,
                         self.displacement_percentage_all_boundary_conditions,
                         self.displacement_percentage_all_boundary_conditions,
                         self.mesh_file, new_cross_section_of_fractures,
                         young_modul_rock_pa,reduced_young_modul_fractures]
        else:
            new_words = [self.displacement_percentage_x, self.displacement_percentage_y,
                         self.displacement_percentage_z, self.mesh_file, new_cross_section_of_fractures,
                         young_modul_rock_pa,reduced_young_modul_fractures]

        with open(self.path_to_yaml_template, 'r') as file:
            # Loads the YAML content
            data_in_template = file.read()

        # Iterates over each pair of old_word and new_word
        for old_word, new_word in zip(old_words, new_words):
            # Replaces each old_word with the corresponding new_word
            data_in_template = data_in_template.replace(old_word, str(new_word))

        # Write the updated content back to the output YAML file
        with open(self.yaml_output_dir, 'w') as file:
            file.write(data_in_template)