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

filename = "C:/Plocha/Bachelor_thesis/Results_and_analysis/Displacement_sequences_analysis/gathered_data_coeffs.txt"  # Adjust the path as needed
result_lists = split_numbers_into_lists(filename)

# Write results to a new file in column vector format
output_filename = "C:/Plocha/Bachelor_thesis/Results_and_analysis/Displacement_sequences_analysis/results_of_analysis.txt"  # Adjust the path as needed

with open(output_filename, 'w') as file:
    for i, list in enumerate(result_lists, start=1):
        file.write(f"c{i}_values:\n")
        for value in list:
            file.write(f"    {value:}\n")
