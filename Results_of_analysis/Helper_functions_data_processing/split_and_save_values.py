def split_numbers_into_lists(path_to_file_with_data):
    # Creates 9 empty lists
    lists = [[] for _ in range(9)]

    with open(path_to_file_with_data, 'r') as file:
        for index, line in enumerate(file, start=1):  # Starts index from 1
            line = line.strip()
            if line:  # Ensures the line is not empty
                number = float(line)
                list_index = (index - 1) % 9  # Matches 1+9i -> list[0], 2+9i -> list[1] and so on...
                lists[list_index].append(number)
    return lists

filename = "C:/Plocha/Bachelor_thesis/Python_scripts/Results_of_analysis/Results_geometry/all_cases_partial_results/case_10/all_coefficients_case_10.txt"  # Adjust the path as needed
result_lists = split_numbers_into_lists(filename)

# Write results to a new file in column vector format
output_filename = "C:/Plocha/Bachelor_thesis/Python_scripts/Results_of_analysis/Results_geometry/all_cases_partial_results/case_10/sorted_all_coefficients_case_10.txt"  # Adjust the path as needed
# Note: The values of C_1 -> C_9 correspond to the values of effective tensor as follows:
#       C_1  C_4  C_7      C_1111   C_1122  C_1112
# C =   C_2  C_5  C_8  =   C_2211   C_2222  C_2212
#       C_3  C_6  C_9      C_1211   C_1222  C1212
with open(output_filename, 'w') as file:
    for i, list in enumerate(result_lists, start=1):
        file.write(f"c{i}_values:\n")
        for value in list:
            file.write(f"    {value:}\n")
