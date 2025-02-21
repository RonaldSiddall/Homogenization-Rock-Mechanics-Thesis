import os
import sys
import time
from Utility_methods.parameter_summaries import parameters_short_summary_print_out_yaml
from Logic_classes.GenerateYaml import GenerateYaml

# This function generates a mesh (.msh file) using the provided configuration file (config_file.yaml)
def create_yaml(config_file, mesh_file):
    try:
        start_time = time.time()
        GenerateYaml(config_file, mesh_file).generate_yaml()
        end_time = time.time()
        name_of_script_yaml = os.path.basename(__file__)
        parameters_short_summary_print_out_yaml(config_file, mesh_file, start_time, end_time, name_of_script_yaml)
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
            print(f"python <{sys.argv[0]}> <config_file.yaml> <mesh_file.msh>\n")
            print("-----------------------------------------------------------------------------")
            # Exit the script with an error status code
            sys.exit(1)

        # Extract the path to the config file from the command-line arguments
        config_file = sys.argv[1]
        mesh_file = sys.argv[2]
        # Calls the main function with the config file path as an argument
        create_yaml(config_file, mesh_file)

    except Exception as error_message:
        # If any error occurs during execution, prints the error message
        print("--------------------------------------------------------------------------------")
        print("\nAn error occurred during execution. The error message is written below:\n")
        print(str(error_message)+"\n")
        print("\n------------------------------------------------------------------------------")