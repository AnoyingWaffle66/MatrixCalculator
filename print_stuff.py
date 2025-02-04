def prettify_matrix(matrix: list, rows: int):
    columns = int(len(matrix)/rows)
    for row in range(0, rows):
        row_to_print = []
        for column in range(0, columns):
            row_to_print.append(matrix[row*columns+column])
        string_no_comma = "["
        for number in range(0, len(row_to_print)):
            number_str = "%.2f" % row_to_print[number]
            string_no_comma += f"{' ' * (7 - len(number_str))}  {number_str}"
            if number == len(row_to_print) - 1:
                string_no_comma += "   ]"
        print(string_no_comma)

def print_matrix(matrix: dict, matrix_name: str):
    print("")
    print(f"name    - {matrix_name}")
    for matrix_sub in matrix:
        if matrix_sub != "values":
            print(f"{matrix_sub} " + " " * (7 - len(matrix_sub)) + f"- {matrix[matrix_sub]}")
        else:
            print("values")
            prettify_matrix(matrix[matrix_sub], matrix["rows"])
    print("")

def print_vector(vector: dict, vector_name: str):
    print("")
    print(f"name  - {vector_name}\n")
    print(prettify_vector(vector["values"]) + "\n")

def prettify_vector(vector: list) -> str:
    vec_string = "< "
    for number in vector:
        number_str = "%.2f" % number
        maximum = 6
        if number_str[0] == "-":
            maximum = 7
        number_str_len = maximum - len(number_str)
        vec_string += f"{' ' * number_str_len}{number_str}{' ' * number_str_len}"
    vec_string += " >"
    return vec_string