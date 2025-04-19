import sys
import time
import os
from Logic_classes.GenerateVtuFiles import GenerateVtuFiles
from Logic_classes.GenerateTensor import GenerateTensor
from Utility_methods.parameter_summaries import parameters_short_summary_print_out_flow

# This function generates a .txt file using the provided configuration file (config_file.yaml) and
# input .yaml file that describes the homogenization problem
def create_file_with_tensor(config_file, yaml_file):
    try:
        start_time = time.time()
        vtu_dirs = GenerateVtuFiles(config_file, yaml_file).extract_vtu_files()
        GenerateTensor(config_file, yaml_file, vtu_dirs).get_tensor_in_txt_formatted()
        end_time = time.time()
        # This extracts the name of the file you are reading now
        name_of_script_flow = os.path.basename(__file__)
        parameters_short_summary_print_out_flow(config_file, yaml_file, start_time, end_time, name_of_script_flow)

        # There wasn't enough time to implement an in-built function for writing the tensor to a file
        # Which is why this quick-solve method is commented out... - but it works
        # coefficients = GenerateTensor(config_file, yaml_file, vtu_dirs).compute_effect_elast_constants_voigt()
        # c1 = coefficients[0][0]
        # c2 = coefficients[0][1]
        # c3 = coefficients[0][2]
        # c4 = coefficients[1][0]
        # c5 = coefficients[1][1]
        # c6 = coefficients[1][2]
        # c7 = coefficients[2][0]
        # c8 = coefficients[2][1]
        # c9 = coefficients[2][2]
        # constants = [c1, c2, c3, c4, c5, c6, c7, c8, c9]
        # with open("C:/Plocha/Bachelor_thesis/Python_scripts/Results_of_analysis/Results_geometry/all_cases_partial_results/case_10/all_coefficients_case_10.txt", "a") as file:
        #    for constant in constants:
        #        file.write(f"{constant}\n")
    except Exception as error_mess:
        # If an error occurs during the execution, this prints the error message
        print("-------------------------------------------------------------------------------")
        print("\nAn error occurred during execution. The error message is written below:\n")
        print(str(error_mess) + "\n")
        print("-------------------------------------------------------------------------------")

if __name__ == "__main__":
    try:
        # Checks if the number of command-line arguments is less than 3
        if len(sys.argv) < 3:
            # If fewer than 3 arguments are provided, this prints out a message
            print("-----------------------------------------------------------------------------")
            print("\nAn error occurred during execution.")
            print("Please make sure to enter the command like this:\n")
            print(f"python <{sys.argv[0]}> <config_file.yaml> <input_yaml_file.yaml>\n")
            print("-----------------------------------------------------------------------------")
            sys.exit(1)

        # Extracts the path to the config file and the input yaml file from the command-line arguments
        config_file = sys.argv[1]
        input_yaml_file = sys.argv[2]
        create_file_with_tensor(config_file, input_yaml_file)

    except Exception as error_message:
        # If any error occurs during execution, prints the error message
        print("--------------------------------------------------------------------------------")
        print("\nAn error occurred during execution. The error message is written below:\n")
        print(str(error_message)+"\n")
        print("\n------------------------------------------------------------------------------")