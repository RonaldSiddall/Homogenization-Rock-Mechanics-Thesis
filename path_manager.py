import os
from ConfigManager import ConfigManager

def get_all_needed_paths_mesh(config_file):
    config = ConfigManager(config_file)
    needed_paths = []
    # Checks if the provided path by the user is relative or absolute
    if not os.path.isabs(config_file):
        # If it is relative, joins it with the project directory path
        config_file_path = os.path.join(config.get_absolute_path_to_dir_with_project(), config_file)
    else:
        config_file_path = config_file

    if config.get_customize_mesh_name() == "yes":
        created_mesh_file_path =  config.get_dir_where_mesh_is_created() + config.get_new_mesh_file_name() + ".msh"
    else:
        created_mesh_file_path =  config.get_dir_where_mesh_is_created() +  "generated_mesh.msh"

    txt_summary_path = config.get_dir_of_where_summary_is_created_mesh()
    # Checks if the provided path by the user is relative or absolute
    if not os.path.isabs(txt_summary_path):
        # If it is relative, joins it with the project directory path
        txt_summary_path = os.path.join(config.get_absolute_path_to_dir_with_project(), txt_summary_path)

    if config.get_change_name_of_txt_file_summary_mesh() == "yes":
        txt_summary_path = os.path.join(txt_summary_path, config.get_new_txt_file_summary_name_mesh() + ".txt")
    else:
        txt_summary_path = os.path.join(txt_summary_path, "parameter_summary.txt")

    needed_paths.append(config_file_path)
    needed_paths.append(str(created_mesh_file_path))
    needed_paths.append(txt_summary_path)
    return needed_paths

def get_all_needed_paths_yaml(config_file, mesh_file):
    config = ConfigManager(config_file)
    needed_paths = []

    # Ensure config_file has an absolute path
    if not os.path.isabs(config_file):
        config_file_path = os.path.join(config.get_absolute_path_to_dir_with_project(), config_file)
    else:
        config_file_path = config_file

    # Ensure mesh_file has an absolute path
    if not os.path.isabs(mesh_file):
        used_mesh_file_path = os.path.join(config.get_absolute_path_to_dir_with_project(), mesh_file).replace("C:", "/C")
    else:
        used_mesh_file_path = mesh_file.replace("C:", "/C")

    # Process YAML template path
    yaml_template_path = config.get_path_to_yaml_template()
    if not os.path.isabs(yaml_template_path):
        yaml_template_path = os.path.join(config.get_absolute_path_to_dir_with_project(), yaml_template_path)

    # Process directory where YAML is created
    yaml_output_dir = config.get_dir_where_yaml_is_created()

    if not os.path.isabs(yaml_output_dir):
        yaml_output_dir = os.path.join(config.get_absolute_path_to_dir_with_project(), yaml_output_dir)
    else:
        yaml_output_dir = yaml_output_dir
    os.makedirs(yaml_output_dir.replace("/C", "C:"), exist_ok=True)
    # Determine the final YAML output file name
    if config.get_change_names_of_computed_yaml() == "yes":
        yaml_output_file = yaml_output_dir + config.get_new_name_of_yaml()
    else:
        yaml_output_file = os.path.join(yaml_output_dir, "generated_yaml.yaml")

    txt_summary_path = config.get_dir_of_where_summary_is_created_yaml()
    if not os.path.isabs(txt_summary_path):
        txt_summary_path = os.path.join(config.get_absolute_path_to_dir_with_project(), txt_summary_path)

    if config.get_change_name_of_txt_file_summary_yaml() == "yes":
        txt_summary_path = os.path.join(txt_summary_path, config.get_new_txt_file_summary_name_yaml() + ".txt")
    else:
        txt_summary_path = os.path.join(txt_summary_path, "parameter_summary.txt")

    # Append the resolved paths to the list
    needed_paths.append(config_file_path)
    needed_paths.append(used_mesh_file_path)
    needed_paths.append(yaml_template_path)
    needed_paths.append(yaml_output_file)
    needed_paths.append(txt_summary_path)
    return needed_paths