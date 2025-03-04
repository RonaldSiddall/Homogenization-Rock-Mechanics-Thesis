import numpy as np
import pyvista as pv
from Logic_classes.ConfigManager import ConfigManager
from Utility_methods.path_manager import get_all_needed_paths_flow

class GenerateTensor:
    def __init__(self, config_file, yaml_file, vtu_dirs):
        self.config = ConfigManager(config_file)
        self.needed_paths_flow = get_all_needed_paths_flow(config_file, yaml_file)
        self.output_dir_of_file_with_tensor = self.needed_paths_flow[3] + ".txt"
        self.boundary_conditions_have_equal_displacement = self.config.get_boundary_conditions_have_equal_displacement()
        self.displacement_percentage_all_boundary_conditions = self.config.get_displacement_percentage_all_boundary_conditions()
        self.displacement_percentage_x = self.config.get_displacement_percentage_x()
        self.displacement_percentage_y = self.config.get_displacement_percentage_y()
        self.displacement_percentage_shear = self.config.get_displacement_percentage_shear()
        self.vtu_dirs = vtu_dirs
        self.meshes = []
        for vtu_file in self.vtu_dirs:
            self.meshes.append(pv.UnstructuredGrid(vtu_file))

    def compute_sigmas(self):
        sigmas = []
        for mesh in self.meshes:
            sigmas.append(mesh.cell_data.get("stress"))
        return sigmas

    def compute_meshes_with_areas(self):
        mesh_with_areas = []
        for mesh in self.meshes:
            mesh_with_areas.append(mesh.compute_cell_sizes(area=True).get_array("Area"))
        return mesh_with_areas

    def compute_effect_elast_constants_voigt(self):
        constants_voigt_list = []
        sigmas = self.compute_sigmas()
        areas = self.compute_meshes_with_areas()
        amount_of_meshes = len(self.meshes)

        for i in range(amount_of_meshes):
            sigma = sigmas[i]
            area = areas[i]
            stress_area = []
            for j in range(len(sigma)):
                stress_area.append(sigma[j, :] * area[j])

            all_constants = np.sum(stress_area, axis=0) / np.sum(area)
            # all_constants: for each load case we get a matrix 3x3 so in total there
            # are 3 matrices with 9 constants => 27 constants
            # in each individual matrix has this form:
            # [a b  0
            #  b c  0
            #  0 0  0]
            # where a, b, c are the effective elastic coefficients
            # because we don't care about zeros in this matrix, so we need to only extract a, b, c
            # that is the reason for the indexes 0, 1, 4 = index 0 - a, index 1 - b, index 4 - c
            needed_indexes = [0, 4, 1]
            # if we look at the 2x2 matrix [a b , b c] then in voigt notation we get [a, b, c]
            # and this vector [a, b, c] for the first load case = first column in the final tensor
            # second case: second column
            # third case: third column
            constants_voigt = [all_constants[index] for index in needed_indexes]
            constants_voigt_list.append(constants_voigt)

        # The values of the constants need to be divided by the displacement
        # The reason is given in the theory, where the effective elastic coefficients are determined mathematically
        coefficients = np.array(constants_voigt_list)
        if self.boundary_conditions_have_equal_displacement == "yes":
            coefficients /= self.displacement_percentage_all_boundary_conditions
        else:
            coefficients[0][0] /= self.displacement_percentage_x
            coefficients[0][1] /= self.displacement_percentage_x
            coefficients[0][2] /= self.displacement_percentage_x
            coefficients[1][0] /= self.displacement_percentage_y
            coefficients[1][1] /= self.displacement_percentage_y
            coefficients[1][2] /= self.displacement_percentage_y
            coefficients[2][0] /= self.displacement_percentage_shear
            coefficients[2][1] /= self.displacement_percentage_shear
            coefficients[2][2] /= self.displacement_percentage_shear

        # the {coefficients[2][0]}, {coefficients[2][1]}, {coefficients[2][2]} need to be divided by two
        # the reason is written in the theory
        coefficients[2][0] = coefficients[2][0] / 2
        coefficients[2][1] = coefficients[2][1] / 2
        coefficients[2][2] = coefficients[2][2] / 2
        coefficients.tolist()

        return coefficients

    def get_tensor_in_txt_formatted(self):
        coefficients = self.compute_effect_elast_constants_voigt()
        with open(self.output_dir_of_file_with_tensor, "w") as txt_file:
            txt_file.write(
                "============================================================================================\n")
            txt_file.write("                    Effective elastic tensor in matrix form for 2D problems\n")
            txt_file.write(
                "============================================================================================\n\n")
            txt_file.write(
                f"            {coefficients[0][0]:<25}           {coefficients[1][0]:<25}      {coefficients[2][0]}\n")
            txt_file.write(
                f"C =         {coefficients[0][1]:<25}         {coefficients[1][1]:<25}       {coefficients[2][1]}\n")
            txt_file.write(
                f"            {coefficients[0][2]:<25}          {coefficients[1][2]:<25}      {coefficients[2][2]}\n\n\n")
            txt_file.write(
                "--------------------------------------------------------------------------------------------\n")
            txt_file.write("This result was computed using these files:\n")
            for vtu_file in self.vtu_dirs:
                txt_file.write(f"{vtu_file}\n")