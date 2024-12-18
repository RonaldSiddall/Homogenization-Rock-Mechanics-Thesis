import os
import numpy as np
import pyvista as pv


def compute_meshes(vtu_dirs):
    meshes = []
    for vtu_file in vtu_dirs:
        meshes.append(pv.UnstructuredGrid(vtu_file))
    return meshes


def compute_sigmas(vtu_dirs):
    meshes = compute_meshes(vtu_dirs)
    sigmas = [mesh.cell_data.get("stress") for mesh in meshes]
    return sigmas


def compute_areas(vtu_dirs):
    meshes = compute_meshes(vtu_dirs)
    areas = [mesh.compute_cell_sizes(area=True).get_array("Area") for mesh in meshes]
    return areas


def compute_effect_elast_constants_voigt(vtu_dirs):
    meshes = compute_meshes(vtu_dirs)
    sigmas = compute_sigmas(vtu_dirs)
    areas = compute_areas(vtu_dirs)
    constants_voigt_list = []

    for i in range(len(meshes)):
        sigma = sigmas[i]
        area = areas[i]
        stress_area = np.array([sigma[j, :] * area[j] for j in range(len(sigma))])
        all_constants = np.sum(stress_area, axis=0) / np.sum(area)
        needed_indexes = [0, 4, 1]
        constants_voigt = [all_constants[index] for index in needed_indexes]
        constants_voigt_list.append(constants_voigt)
    return constants_voigt_list


def get_tensor_in_txt_formatted(output_dir, file_name, vtu_dirs):
    coefficients = compute_effect_elast_constants_voigt(vtu_dirs)
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{file_name}.txt")

    with open(file_path, "w") as txt_file:
        txt_file.write("=========================================================================================="  + "\n")
        txt_file.write("                    Effective elastic tensor in matrix form for 2D problems with DFN \n")
        txt_file.write("=========================================================================================="  + "\n\n")
        txt_file.write(
            f"            {coefficients[0][0]}           {coefficients[1][0]}       {coefficients[2][0] / 2}\n"
        )
        txt_file.write(
            f"C =         {coefficients[0][1]}         {coefficients[1][1]}       {coefficients[2][1] / 2}\n"
        )
        txt_file.write(
            f"            {coefficients[0][2]}          {coefficients[1][2]}       {coefficients[2][2] / 2}\n\n"
        )
        txt_file.write("------------------------------------------------------------------------------------------" + "\n")
        txt_file.write("This result was computed using these files:\n")
        for vtu_dir in vtu_dirs:
            txt_file.write(f"{vtu_dir}\n")
        print(f"The effective elastic tensor has been written into the file {os.path.join(output_dir, file_name)}.txt")

get_tensor_in_txt_formatted(
    output_dir=r"C:\Plocha\Bachelor_thesis\Python_scripts\simulation_results_compression",
    file_name="effective_elastic_tensor_compression",
    vtu_dirs =
    [
        r"C:\Plocha\Bachelor_thesis\Python_scripts\simulation_results_compression\output\mechanics\mechanics-000000.vtu",
        r"C:\Plocha\Bachelor_thesis\Python_scripts\simulation_results_compression\output\mechanics\mechanics-000001.vtu",
        r"C:\Plocha\Bachelor_thesis\Python_scripts\simulation_results_compression\output\mechanics\mechanics-000002.vtu",
    ]
)
