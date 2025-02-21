from Logic_classes.ConfigManager import ConfigManager

# This method validates the parameters loaded from the config file used for creating the .msh file.
# If any parameter is invalid, the method ends and returns False
def check_values_in_config_file_mesh(config_file):
    # Loading from config
    config = ConfigManager(config_file)
    rectangle_dimensions = config.get_rectangle_dimensions()
    sample_range = config.get_sample_range()
    k_r = config.get_k_r()
    diam_range = config.get_diam_range()
    p32_r0_to_r_infty = config.get_p32_r0_to_r_infty()
    fisher_trend = config.get_fisher_trend()
    fisher_plunge = config.get_fisher_plunge()
    fisher_kappa = config.get_fisher_kappa()
    von_mises_trend = config.get_von_mises_trend()
    von_mises_kappa = config.get_von_mises_kappa()
    tolerance_initial_delaunay = config.get_tolerance_initial_delaunay()
    tolerance = config.get_tolerance()
    tolerance_boolean = config.get_tolerance_boolean()
    fracture_mesh_step = config.get_fracture_mesh_step()

    control_variable = True
    if rectangle_dimensions[0] <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: Invalid rectangle x dimension [{rectangle_dimensions[0]}, {rectangle_dimensions[1]}].\nReason: Rectangle dimensions must be greater than zero.")
        print("===============================================================================\n")
        control_variable = False
    elif rectangle_dimensions[1] <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: Invalid rectangle y dimension [{rectangle_dimensions[0]}, {rectangle_dimensions[1]}].\nReason: Rectangle dimensions must be greater than zero.")
        print("===============================================================================\n")
        control_variable = False
    elif sample_range[0] <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: The sample_range interval [r_min, r_max] = [{sample_range[0]}, {sample_range[1]}] is invalid.")
        print(f"Reason: r_min must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    elif sample_range[1] <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: The sample_range interval [r_min, r_max] = [{sample_range[0]}, {sample_range[1]}] is invalid.\nReason: r_max must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    elif sample_range[1] <= sample_range[0]:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: The sample_range interval [r_min, r_max] = [{sample_range[0]}, {sample_range[1]}] is invalid.\nReason: r_min must be smaller than r_max.")
        print("===============================================================================\n")
        control_variable = False
    elif k_r <= 2:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: k_r = {k_r} is invalid.\nReason: k_r must be greater than 2.")
        print("===============================================================================\n")
        control_variable = False
    elif diam_range[0] <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: The diam_range interval [r_0, r_infinity] = [{diam_range[0]}, {diam_range[1]}] is invalid.\nReason: r_0 must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    elif diam_range[1] <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: The diam_range interval [r_0, r_infinity] = [{diam_range[0]}, {diam_range[1]}] is invalid.\nReason: r_infinity must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    elif diam_range[1] <= diam_range[0]:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: The diam_range interval [r_0, r_infinity] = [{diam_range[0]}, {diam_range[1]}] is invalid.\nReason: r_0 must be smaller than r_infinity.")
        print("===============================================================================\n")
        control_variable = False
    elif p32_r0_to_r_infty <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: p32_r0_to_r_infty = {p32_r0_to_r_infty} is invalid.\nReason: p32_r0_to_r_infty must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    elif fisher_trend > 360 or fisher_trend < 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: fisher_trend = {fisher_trend} is invalid.\nReason: fisher_trend must lie within the interval [0, 360].")
        print("===============================================================================\n")
        control_variable = False
    elif fisher_plunge > 90 or fisher_plunge < 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: fisher_plunge = {fisher_plunge} is invalid.\nReason: fisher_plunge must lie within the interval [0, 90].")
        print("===============================================================================\n")
        control_variable = False
    elif fisher_kappa < 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: fisher_kappa = {fisher_kappa} is invalid.\nReason: fisher_kappa must be greater or equal to 0.")
        print("===============================================================================\n")
        control_variable = False
    elif von_mises_trend < 0 or von_mises_trend > 360:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: von_mises_trend = {von_mises_trend} is invalid.\nReason: von_mises_trend must lie within the interval [0, 360].")
        print("===============================================================================\n")
        control_variable = False
    elif von_mises_kappa < 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: von_mises_kappa = {von_mises_kappa} is invalid.\nReason: von_mises_kappa must be greater or equal to 0.")
        print("===============================================================================\n")
        control_variable = False
    elif tolerance_initial_delaunay <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: tolerance_initial_delaunay = {tolerance_initial_delaunay} is invalid.\nReason: tolerance_initial_delaunay must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    elif tolerance <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: tolerance = {tolerance} is invalid.\nReason: tolerance must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    elif tolerance_boolean <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: tolerance_boolean = {tolerance_boolean} is invalid.\nReason: tolerance_boolean must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    elif fracture_mesh_step <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: fracture_mesh_step = {fracture_mesh_step} is invalid.\nReason: fracture_mesh_step must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    return control_variable

# This method validates the parameters loaded from the config file used for creating the .yaml file.
# If any parameter is invalid, the method ends and returns False
def check_values_in_config_file_yaml(config_file):
    # Loading of the parameters from the config file
    config = ConfigManager(config_file)
    boundary_conditions_have_equal_displacement = config.get_boundary_conditions_have_equal_displacement()
    displacement_percentage_all_boundary_conditions = config.get_displacement_percentage_all_boundary_conditions()
    displacement_percentage_x = config.get_displacement_percentage_x()
    displacement_percentage_y = config.get_displacement_percentage_y()
    displacement_percentage_shear = config.get_displacement_percentage_shear()
    cross_section_multiplier = config.get_cross_section_multiplier()
    young_modul_rock_gpa = config.get_young_modul_rock_gpa()
    reduction_value_for_fractures = config.get_reduction_value_for_fractures()

    control_variable = True

    if abs(displacement_percentage_all_boundary_conditions) >= 1:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: displacement_percentage_all_boundary_conditions = {displacement_percentage_all_boundary_conditions} is invalid.\nReason: displacement_percentage_all_boundary_conditions must be between 0 and 1.")
        print("===============================================================================\n")
        control_variable = False
    elif abs(displacement_percentage_x) >= 1:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: displacement_percentage_x = {displacement_percentage_x} is invalid.\nReason: displacement_percentage_x must be between 0 and 1.")
        print("===============================================================================\n")
        control_variable = False
    elif abs(displacement_percentage_y) >= 1:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: displacement_percentage_y = {displacement_percentage_y} is invalid.\nReason: displacement_percentage_y must be between 0 and 1.")
        print("===============================================================================\n")
        control_variable = False
    elif abs(displacement_percentage_shear) >= 1:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: displacement_percentage_shear = {displacement_percentage_shear} is invalid.\nReason: displacement_percentage_shear must be between 0 and 1.")
        print("===============================================================================\n")
        control_variable = False
    elif cross_section_multiplier <= 0 or cross_section_multiplier > 1:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: cross_section_multiplier = {cross_section_multiplier} is invalid.\nReason: cross_section_multiplier must be greater than 0 and less than 1.")
        print("===============================================================================\n")
        control_variable = False
    elif young_modul_rock_gpa <= 0:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: young_modul_rock_gpa = {young_modul_rock_gpa} is invalid.\nReason: young_modul_rock_gpa must be greater than 0.")
        print("===============================================================================\n")
        control_variable = False
    elif reduction_value_for_fractures <= 1:
        print("\n===============================================================================")
        print("Parameter validation in configuration file failed.")
        print("See error message below and try again with correct parameter values:\n")
        print(f"Error: reduction_value_for_fractures = {reduction_value_for_fractures} is invalid.\nReason: reduction_value_for_fractures must be greater than 1.")
        print("===============================================================================\n")
        control_variable = False
    return control_variable