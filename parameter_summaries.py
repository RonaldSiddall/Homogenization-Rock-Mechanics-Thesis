from ConfigManager import ConfigManager
from path_manager import get_all_needed_paths_mesh, get_all_needed_paths_yaml

def parameters_short_summary_print_out_mesh(config_file, fracture_set):
    config = ConfigManager(config_file)
    needed_paths = get_all_needed_paths_mesh(config_file)
    if config.get_create_complete_summary_txt_file_mesh() == "yes":
        print("\n\n")
        print("======================================= MESH AND FRACTURE NETWORK CREATED SUCCESSFULLY =======================================")
        print("Script used: ")
        print("  - create_mesh.py")
        print("Input:")
        print(f"  - Config file used: {needed_paths[0]}")
        print("Output:")
        print(f"  - Mesh file created: {needed_paths[1]}")
        print(f"  - Healed mesh file created: {needed_paths[1].replace('.msh', '_healed.msh')}")
        print(f"  - File with complete summary created: {needed_paths[2]}")
        print("==============================================================================================================================")
        write_parameters_info_to_file_mesh(config_file, fracture_set)
    else:
            print("\n\n")
            print("======================================= MESH AND FRACTURE NETWORK CREATED SUCCESSFULLY =======================================")
            print("Script used: ")
            print("  - create_mesh.py")
            print("Input:")
            print(f"  - Config file used: {needed_paths[0]}")
            print("Output:")
            print(f"  - Mesh file created: {needed_paths[1]}")
            print(f"  - Healed mesh file created: {needed_paths[1].replace('.msh', '_healed.msh')}")
            print("==============================================================================================================================")


def write_parameters_info_to_file_mesh(config_file, fracture_set):
    config = ConfigManager(config_file)
    needed_paths = get_all_needed_paths_mesh(config_file)
    txt_summary_path = needed_paths[2]
    rectangle_dimensions = config.get_rectangle_dimensions()
    summary = [
        "=" * 70,
        " " * 25 + "MESH CREATION SUMMARY",
        "=" * 70,
        "SCRIPT USED:",
        "  - create_mesh.py",
        "INPUT:",
        f"  - Config file used: {needed_paths[0]}",
        "OUTPUT:",
        f"  - Mesh file created       : {needed_paths[1]}",
        f"  - Healed mesh file created: {needed_paths[1].replace('.msh', '_healed.msh')}",
        "-" * 70,
        "INFORMATION ABOUT THE CREATED FRACTURE NETWORK",
        f"  - Number of fractures created: {len(fracture_set)}",
        f"  - Rectangle dimensions       : {rectangle_dimensions}",
        f"  - Domain                     : [{rectangle_dimensions[0]}, {rectangle_dimensions[1]}, 0]",
        f"  - Diam range                 : {config.get_diam_range()}",
        f"  - Sample range               : {config.get_sample_range()}",
        f"  - k_r                        : {config.get_k_r()}",
        f"  - p32_r_0_to_infty           : {config.get_p32_r0_to_r_infty()}",
        "-" * 70,
        "FISHER ORIENTATION PARAMETERS",
        f"  - Fisher trend  : {config.get_fisher_trend()}",
        f"  - Fisher plunge : {config.get_fisher_plunge()}",
        f"  - Fisher kappa  : {config.get_fisher_kappa()}",
        "-" * 70,
        "VON MISES PARAMETERS",
        f"  - Von Mises trend : {config.get_von_mises_trend()}",
        f"  - Von Mises kappa : {config.get_von_mises_kappa()}",
        "-" * 70,
        "GMSH OPTIONS PARAMETERS",
        f"  - Fracture mesh step          : {config.get_fracture_mesh_step()}",
        f"  - Tolerance (Initial Delaunay): {config.get_tolerance_initial_delaunay()}",
        f"  - GMSH Tolerance Boolean      : {config.get_tolerance_boolean()}",
        f"  - GMSH Tolerance              : {config.get_tolerance()}",
        "=" * 70
    ]

    # Writes the formatted summary to the .txt file
    with open(txt_summary_path, "w") as file:
        file.write("\n".join(summary))

def parameters_short_summary_print_out_yaml(config_file, mesh_file):
    config = ConfigManager(config_file)
    needed_paths = get_all_needed_paths_yaml(config_file, mesh_file)
    if config.get_create_complete_summary_txt_file_yaml() == "yes":
        print("\n")
        print("======================================= YAML FILE FOR HOMOGENIZATION CREATED SUCCESSFULLY =======================================")
        print("Script used: ")
        print("  - create_yaml.py")
        print("Input:")
        print(f"  - Config file used: {needed_paths[0]}")
        print(f"  - Mesh file used: {needed_paths[1]}")
        print(f"  - YAML template used: {needed_paths[2]}")
        print("Output:")
        print(f"  - Created YAML: {needed_paths[3]}")
        print(f"  - File with complete summary created: {needed_paths[4]}")
        print("=================================================================================================================================")
        write_parameters_info_to_file_yaml(config_file, mesh_file)
    else:
        print("\n")
        print("======================================= YAML FILE FOR HOMOGENIZATION CREATED SUCCESSFULLY =======================================")
        print("Script used: ")
        print("  - create_yaml.py")
        print("Input:")
        print(f"  - Config file used: {needed_paths[0]}")
        print(f"  - Mesh file used: {needed_paths[1]}")
        print(f"  - YAML template used: {needed_paths[2]}")
        print("Output:")
        print(f"  - Created YAML: {needed_paths[3]}")
        print("=================================================================================================================================")

def write_parameters_info_to_file_yaml(config_file, mesh_file):
    config = ConfigManager(config_file)
    needed_paths = get_all_needed_paths_yaml(config_file, mesh_file)
    txt_summary_path = needed_paths[4]
    rectangle_dimensions = config.get_rectangle_dimensions()
    summary = [
        "=" * 70,
        " " * 25 + "YAML CREATION SUMMARY",
        "=" * 70,
        "SCRIPT USED:",
        "  - create_yaml.py",
        "INPUT:",
        f"  - Config file used: {needed_paths[0]}",
        f"  - Mesh file used: {needed_paths[1]}",
        f"  - YAML template used: {needed_paths[2]}",
        "OUTPUT:",
        f"  - YAML file created: {needed_paths[3]}",
        "-" * 70,
        "HOMOGENIZATION PARAMETERS",
        f"  - Cross section: {config.get_cross_section_multiplier()*rectangle_dimensions[0]*rectangle_dimensions[1]}",
        f"  - Young modulus of rock (Pa): {config.get_young_modul_rock_gpa()*1000}",
        f"  - Young modulus of fractures (Pa): {config.get_young_modul_rock_gpa()*1000/config.get_reduction_value_for_fractures()}",
        "-" * 70,
    ]

    # Writes the formatted summary to the .txt file
    with open(txt_summary_path, "w") as file:
        file.write("\n".join(summary))