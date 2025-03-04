import subprocess
import os
from ruamel.yaml import YAML
yaml = YAML()
from Logic_classes.ConfigManager import ConfigManager
from Utility_methods.path_manager import get_all_needed_paths_flow

class GenerateVtuFiles:
    # Initiation of the used parameters from the config.yaml file or necessary paths
    def __init__(self, config_file, yaml_file):
        self.config = ConfigManager(config_file)
        needed_paths_flow = get_all_needed_paths_flow(config_file, yaml_file)
        self.input_yaml_file_path = needed_paths_flow[1]
        self.simulation_output_dir = needed_paths_flow[2]
        self.bat_file_path = needed_paths_flow[4]
        self.display_std_output_flow = self.config.get_display_std_output()

    def run_simulation(self):
        # The command below can be uncommented (as well as the method 'delete_directory_contents' at the bottom of the file)
        # in the case the user wishes to delete everything within the directory
        # self.delete_directory_contents(self.simulation_output_dir.replace("/C","C:"))

        # This command runs the flow123d simulator
        # -s -- solves for given yaml_path
        # -o -- defines the output_path where the results should be saved
        command_to_run_flow123d_simulation = [self.bat_file_path, "-s", self.input_yaml_file_path, "-o", self.simulation_output_dir]
        if self.display_std_output_flow == "yes":
            subprocess.run(command_to_run_flow123d_simulation, shell=True)
        else:
            print("***************************************************************************")
            print("[SIMULATION] RUNNING SIMULATIONS AND COMPUTING EFFECTIVE ELASTIC TENSOR...")
            print("***************************************************************************")
            subprocess.run(command_to_run_flow123d_simulation, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # This method returns a list of the .vtu files that have been created by the flow123d simulator
    def extract_vtu_files(self):
        self.run_simulation()
        mechanics_dir = os.path.join(self.simulation_output_dir, "mechanics").replace("\\","/").replace("/C","C:")

        extracted_files = [os.path.join(mechanics_dir, f) for f in os.listdir(mechanics_dir)]
        for i in range(len(extracted_files)):
            extracted_files[i] = extracted_files[i].replace("\\", "/")
        return extracted_files