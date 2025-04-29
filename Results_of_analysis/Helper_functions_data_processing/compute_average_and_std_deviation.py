import math

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

def compute_average(values):
    return sum(values) / len(values)

def compute_standard_deviation(values, average):
    variance = sum((x - average) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


path_to_file_with_data = "C:/Plocha/Bachelor_thesis/Results_and_analysis/Dependence_tensor_on_cross_section/tension_0_07/tension_gathered_results_cross_section.txt"
result_lists = split_numbers_into_lists(path_to_file_with_data)

# Writes the results into a new file in column vector format
output_path_to_file_with_data = "C:/Plocha/Bachelor_thesis/Results_and_analysis/Dependence_tensor_on_cross_section/tension_0_07/tension_statistics_cross_section.txt"

with open(output_path_to_file_with_data, 'w') as file:
    for i, values in enumerate(result_lists, start=1):
        file.write(f"c{i}_values:\n")
        for value in values:
            file.write(f"    {value:}\n")

        average = compute_average(values)
        standard_deviation = compute_standard_deviation(values, average)

        file.write(f"  Average: {average}\n")
        file.write(f"  Standard Deviation: {standard_deviation}\n\n")
