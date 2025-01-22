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