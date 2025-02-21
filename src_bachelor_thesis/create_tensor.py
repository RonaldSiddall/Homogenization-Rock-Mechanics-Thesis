import sys
from src_bachelor_thesis.Logic_classes.GenerateVtuFiles import GenerateVtuFiles
from src_bachelor_thesis.Logic_classes.GenerateTensor import GenerateTensor
from src_bachelor_thesis.Utility_methods.parameter_summaries import parameters_short_summary_print_out_flow
import time
import os

# This function generates a .txt file using the provided configuration file (config_file.yaml) and
# input yaml file that describes the homogenization problem
def create_file_with_tensor(config_file, yaml_file):
    try:
        start_time = time.time()
        vtu_dirs = GenerateVtuFiles(config_file, yaml_file).extract_vtu_files()
        GenerateTensor(config_file, yaml_file, vtu_dirs).get_tensor_in_txt_formatted()
        end_time = time.time()
        # this extracts the name of the file you are reading now
        name_of_script_flow = os.path.basename(__file__)
        parameters_short_summary_print_out_flow(config_file, yaml_file, start_time, end_time, name_of_script_flow)
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