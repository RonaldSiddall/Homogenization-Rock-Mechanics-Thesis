import os
import sys
import time
from Logic_classes.GenerateFractures import GenerateFractures
from Logic_classes.GenerateMesh import GenerateMesh
from Utility_methods.parameter_summaries import parameters_short_summary_print_out_mesh
from Utility_methods.check_values_in_config_file import check_values_in_config_file_mesh

# This function generates a mesh (.msh file) using the provided configuration file (config_file.yaml)
def create_mesh(config_file):
    # Checks the relevant values of the parameters used to create the .msh file
    # If at least one parameter is invalid (False is returned) then method stops immediately
    if check_values_in_config_file_mesh(config_file):
        try:
            start_time = time.time()
            fracture_set = GenerateFractures(config_file).generator_of_fracture_set()
            GenerateMesh(config_file, fracture_set).make_mesh()
            end_time = time.time()
            name_of_script_mesh = os.path.basename(__file__)
            parameters_short_summary_print_out_mesh(config_file, fracture_set, start_time, end_time, name_of_script_mesh)
        except Exception as error_mess:
            # If an error occurs during the execution, this prints the error message
            print("-------------------------------------------------------------------------------")
            print("\nAn error occurred during execution. The error message is written below:\n")
            print(str(error_mess) + "\n")
            print("-------------------------------------------------------------------------------")

if __name__ == "__main__":
    try:
        # Checks if the number of command-line arguments is less than 2
        if len(sys.argv) < 2:
            # If fewer than 2 arguments are provided, this prints out a message
            print("-----------------------------------------------------------------------------")
            print("\nAn error occurred during execution.")
            print("Please make sure to enter the command like this:\n")
            print(f"python <{sys.argv[0]}> <config_file.yaml>\n")
            print("-----------------------------------------------------------------------------")
            # Exit the script with an error status code
            sys.exit(1)

        # Extract the path to the config file from the command-line arguments
        config_file = sys.argv[1]

        # Calls the main function with the config file path as an argument
        create_mesh(config_file)

    except Exception as error_message:
        # If any error occurs during execution, prints the error message
        print("--------------------------------------------------------------------------------")
        print("\nAn error occurred during execution. The error message is written below:\n")
        print(str(error_message)+"\n")
        print("\n------------------------------------------------------------------------------")