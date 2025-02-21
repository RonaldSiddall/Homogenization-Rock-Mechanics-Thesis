from datetime import datetime
from Logic_classes.ConfigManager import ConfigManager
from Utility_methods.path_manager import get_all_needed_paths_mesh, get_all_needed_paths_yaml, get_all_needed_paths_flow

def parameters_short_summary_print_out_mesh(config_file, fracture_set, start_time, end_time, name_of_script_mesh):
    config = ConfigManager(config_file)
    needed_paths_mesh = get_all_needed_paths_mesh(config_file)
    if config.get_create_complete_summary_txt_file_mesh() == "yes":
        print("\n\n")
        print("======================================= MESH AND FRACTURE NETWORK CREATED SUCCESSFULLY =======================================")
        print("Script used: ")
        print(f"  - {name_of_script_mesh}")
        print("Input:")
        print(f"  - Config file used: {needed_paths_mesh[0]}")
        print("Output:")
        print(f"  - Mesh file created: {needed_paths_mesh[1]}")
        print(f"  - Healed mesh file created: {needed_paths_mesh[1].replace('.msh', '_healed.msh')}")
        corrected_path = needed_paths_mesh[2].replace("\\", "/")
        print(f"  - File with complete summary created: {corrected_path}")
        elapsed_time = end_time - start_time
        start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Additional information:")
        print(f"  - Process started at: {start_time_str}")
        print(f"  - Process finished at: {end_time_str}")
        print(f"  - Total running time: {elapsed_time:.2f} seconds")
        print("==============================================================================================================================")
        write_parameters_info_to_file_mesh(config_file, fracture_set, start_time, end_time, name_of_script_mesh)
    else:
            print("\n\n")
            print("======================================= MESH AND FRACTURE NETWORK CREATED SUCCESSFULLY =======================================")
            print("Script used: ")
            print(f"  - {name_of_script_mesh}.py")
            print("Input:")
            print(f"  - Config file used: {needed_paths_mesh[0]}")
            print("Output:")
            print(f"  - Mesh file created: {needed_paths_mesh[1]}")
            print(f"  - Healed mesh file created: {needed_paths_mesh[1].replace('.msh', '_healed.msh')}")
            elapsed_time = end_time - start_time
            start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
            end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Additional information:")
            print(f"  - Process started at: {start_time_str}")
            print(f"  - Process finished at: {end_time_str}")
            print(f"  - Total running time: {elapsed_time:.2f} seconds")
            print("==============================================================================================================================")


def write_parameters_info_to_file_mesh(config_file, fracture_set, start_time, end_time, name_of_script_mesh):
    config = ConfigManager(config_file)
    needed_paths_mesh = get_all_needed_paths_mesh(config_file)
    txt_summary_path = needed_paths_mesh[2]
    rectangle_dimensions = config.get_rectangle_dimensions()
    elapsed_time = end_time - start_time
    start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

    summary = [
        "=" * 70,
        " " * 25 + "MESH CREATION SUMMARY",
        "=" * 70,
        "SCRIPT USED:",
        f"  - {name_of_script_mesh}",
        "INPUT:",
        f"  - Config file used: {needed_paths_mesh[0]}",
        "OUTPUT:",
        f"  - Mesh file created       : {needed_paths_mesh[1]}",
        f"  - Healed mesh file created: {needed_paths_mesh[1].replace('.msh', '_healed.msh')}",
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
        "ADDITIONAL INFORMATION",
        f"  - Process started at: {start_time_str}",
        f"  - Process finished at: {end_time_str}",
        f"  - Total running time: {elapsed_time:.2f} seconds",
        "=" * 70
    ]

    # Writes the formatted summary to the .txt file
    with open(txt_summary_path, "w") as file:
        file.write("\n".join(summary))

def parameters_short_summary_print_out_yaml(config_file, mesh_file, start_time, end_time, name_of_script_yaml):
    config = ConfigManager(config_file)
    needed_paths_yaml = get_all_needed_paths_yaml(config_file, mesh_file)

    if config.get_create_complete_summary_txt_file_yaml() == "yes":
        print("\n")
        print("======================================= YAML FILE FOR HOMOGENIZATION CREATED SUCCESSFULLY =======================================")
        print("Script used: ")
        print(f"  - {name_of_script_yaml}")
        print("Input:")
        print(f"  - Config file used: {needed_paths_yaml[0]}")
        corrected_mesh_path = needed_paths_yaml[1].replace("/C","C:")
        print(f"  - Mesh file used: {corrected_mesh_path}")
        print(f"  - YAML template used: {needed_paths_yaml[2]}")
        print("Output:")
        corrected_yaml_path = needed_paths_yaml[3].replace("/C","C:")
        print(f"  - Created YAML: {corrected_yaml_path}")
        corrected_txt_path = needed_paths_yaml[4].replace("\\","/")
        print(f"  - File with complete summary created: {corrected_txt_path}")
        elapsed_time = end_time - start_time
        start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Additional information:")
        print(f"  - Process started at: {start_time_str}")
        print(f"  - Process finished at: {end_time_str}")
        print(f"  - Total running time: {elapsed_time:.2f} seconds")
        print("=================================================================================================================================")
        write_parameters_info_to_file_yaml(config_file, mesh_file, start_time, end_time, name_of_script_yaml)
    else:
        print("\n")
        print("======================================= YAML FILE FOR HOMOGENIZATION CREATED SUCCESSFULLY =======================================")
        print("Script used: ")
        print(f"  - {name_of_script_yaml}")
        print("Input:")
        print(f"  - Config file used: {needed_paths_yaml[0]}")
        print(f"  - Mesh file used: {needed_paths_yaml[1]}")
        print(f"  - YAML template used: {needed_paths_yaml[2]}")
        print("Output:")
        print(f"  - Created YAML: {needed_paths_yaml[3]}")
        elapsed_time = end_time - start_time
        start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Additional information:")
        print(f"  - Process started at: {start_time_str}")
        print(f"  - Process finished at: {end_time_str}")
        print(f"  - Total running time: {elapsed_time:.2f} seconds")
        print("=================================================================================================================================")

def write_parameters_info_to_file_yaml(config_file, mesh_file, start_time, end_time, name_of_script_yaml):
    config = ConfigManager(config_file)
    needed_paths_yaml = get_all_needed_paths_yaml(config_file, mesh_file)
    txt_summary_path = needed_paths_yaml[4]
    rectangle_dimensions = config.get_rectangle_dimensions()
    elapsed_time = end_time - start_time
    start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
    corrected_mesh_path = needed_paths_yaml[1].replace("/C","C:")
    corrected_yaml_path = needed_paths_yaml[3].replace("/C","C:")
    boundary_conditions_have_equal_displacement = config.get_boundary_conditions_have_equal_displacement()
    displacement_percentage_all_boundary_conditions = config.get_displacement_percentage_all_boundary_conditions()
    displacement_percentage_x = config.get_displacement_percentage_x()
    displacement_percentage_y = config.get_displacement_percentage_y()
    displacement_percentage_shear = config.get_displacement_percentage_shear()
    displacement_status = {}
    displacement_values_dict = {
        "x": displacement_percentage_x,
        "y": displacement_percentage_y,
        "shear": displacement_percentage_shear,
        "all": displacement_percentage_all_boundary_conditions
        }
    for axis, value in displacement_values_dict.items():
        if value > 0:
            displacement_status[axis] = "expansion"
        elif value < 0:
            displacement_status[axis] = "compression"
        else:
            displacement_status[axis] = "no displacement"
    x_status = displacement_status["x"]
    y_status = displacement_status["y"]
    shear_status = displacement_status["shear"]
    all_status = displacement_status["all"]

    if boundary_conditions_have_equal_displacement == "yes":
        summary = [
            "=" * 70,
            " " * 25 + "YAML CREATION SUMMARY",
            "=" * 70,
            "SCRIPT USED:",
            f"  - {name_of_script_yaml}",
            "INPUT:",
            f"  - Config file used: {needed_paths_yaml[0]}",
            f"  - Mesh file used: {corrected_mesh_path}",
            f"  - YAML template used: {needed_paths_yaml[2]}",
            "OUTPUT:",
            f"  - YAML file created: {corrected_yaml_path}",
            "-" * 70,
            "HOMOGENIZATION PARAMETERS",
            f"  - Displacement percentage used for all boundary conditions: {displacement_percentage_all_boundary_conditions} ({abs(displacement_percentage_all_boundary_conditions) * 100}% {all_status})",
            f"  - Cross section: {config.get_cross_section_multiplier()*rectangle_dimensions[0]*rectangle_dimensions[1]}",
            f"  - Young modulus of rock: {config.get_young_modul_rock_gpa()*1000} Pascals",
            f"  - Young modulus of fractures: {config.get_young_modul_rock_gpa()*1000/config.get_reduction_value_for_fractures()} Pascals",
            "-" * 70,
            "ADDITIONAL INFORMATION",
            f"  - Process started at: {start_time_str}",
            f"  - Process finished at: {end_time_str}",
            f"  - Total running time: {elapsed_time:.2f} seconds",
            "-" * 70,
        ]

        # Writes the formatted summary to the .txt file
        with open(txt_summary_path, "w") as file:
            file.write("\n".join(summary))
    else:
        summary = [
            "=" * 70,
            " " * 25 + "YAML CREATION SUMMARY",
            "=" * 70,
            "SCRIPT USED:",
            f"  - {name_of_script_yaml}",
            "INPUT:",
            f"  - Config file used: {needed_paths_yaml[0]}",
            f"  - Mesh file used: {corrected_mesh_path}",
            f"  - YAML template used: {needed_paths_yaml[2]}",
            "OUTPUT:",
            f"  - YAML file created: {corrected_yaml_path}",
            "-" * 70,
            "HOMOGENIZATION PARAMETERS",
            f"  - Displacement percentages were not chosen to be the same for all boundary conditions.",
            f"  - Specific displacement percentages are written below for corresponding boundary conditions:",
            f"       - Displacement_x: {displacement_percentage_x} (ie {abs(displacement_percentage_x) * 100:.2f}% {x_status})",
            f"       - Displacement_y: {displacement_percentage_y} (ie {abs(displacement_percentage_y) * 100:.2f}% {y_status})",
            f"       - Displacement_z: {displacement_percentage_shear} (ie {abs(displacement_percentage_shear) * 100:.2f}% {shear_status})",
            f"  - Cross section: {config.get_cross_section_multiplier() * rectangle_dimensions[0] * rectangle_dimensions[1]}",
            f"  - Young modulus of rock: {config.get_young_modul_rock_gpa() * 1000} Pascals",
            f"  - Young modulus of fractures: {config.get_young_modul_rock_gpa() * 1000 / config.get_reduction_value_for_fractures()} Pascals",
            "-" * 70,
            "ADDITIONAL INFORMATION",
            f"  - Process started at: {start_time_str}",
            f"  - Process finished at: {end_time_str}",
            f"  - Total running time: {elapsed_time:.2f} seconds",
            "-" * 70,
        ]

        # Writes the formatted summary to the .txt file
        with open(txt_summary_path, "w") as file:
            file.write("\n".join(summary))

def parameters_short_summary_print_out_flow(config_file, yaml_file, start_time, end_time, name_of_script_flow):
    needed_paths_flow = get_all_needed_paths_flow(config_file, yaml_file)
    print("\n")
    print("======================================= SIMULATION WAS SUCCESSFUL, FINAL TENSOR COMPUTED AND SAVED =======================================")
    print("Script used: ")
    print(f"  - {name_of_script_flow}")
    print("Input:")
    print(f"  - Flow123d .bat file used for simulation: {needed_paths_flow[4]}")
    print(f"  - Config file used: {needed_paths_flow[0]}")
    corrected_input_yaml = needed_paths_flow[1].replace("/C", "C:")
    print(f"  - YAML file used for simulation: {corrected_input_yaml}")
    print("Output:")
    corrected_output_directory_simulation = needed_paths_flow[2].replace("/C", "C:")
    print(f"  - Simulation output: {corrected_output_directory_simulation}")
    print(f"  - File with computed effective elastic tensor: {needed_paths_flow[3]}.txt")
    elapsed_time = end_time - start_time
    start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Additional information:")
    print(f"  - Process started at: {start_time_str}")
    print(f"  - Process finished at: {end_time_str}")
    print(f"  - Total running time: {elapsed_time:.2f} seconds")
    print("==========================================================================================================================================")