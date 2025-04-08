# Given 9 values
values = [
-518.6826019056798,
-20.811975767369667,
9.731518683093894,
-23.935778552490294,
-746.46241310238,
-47.35780311372047,
-37.01856354052072,
-82.50899515042785,
-184.95633514966423
]
if len(values) != 9:
    print("Error: Exactly 9 values are required.")
else:
    # Get user input for division
    try:
        divisor = -0.11
        if divisor == 0:
            print("Error: Cannot divide by zero.")
        else:
            # Divide values by the given number
            divided_values = [v / divisor for v in values]

            # Formatting the matrix
            formatted_matrix = f"""
            {divided_values[0]:<25} {divided_values[3]:<25} {divided_values[6]:<25}
C =         {divided_values[1]:<25} {divided_values[4]:<25} {divided_values[7]:<25}
            {divided_values[2]:<25} {divided_values[5]:<25} {divided_values[8]:<25}
    """
            print(f"Divisor: {divisor}")
            for v in values:
                print(v)
            # Print the formatted matrix
            print("Matrix format:")
            print(formatted_matrix)

            # Print values vertically
            print("Values listed vertically:")
            for val in divided_values:
                print(val)

    except ValueError:
        print("Error: Please enter a valid number.")