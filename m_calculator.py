import json

# "database" file name
file_name = "matrix.json"
empty_file_matrix = {
    "default" : {
        "rows" : 0,
        "columns" : 0,
        "Values" : []
    }
}


# file stuff
def add_to_file(matrix: dict, matrix_name: str):
    matrix_objs = get_matrices_from_file()
    if not matrix_objs:
        print("OH NO IS BROKEN")
        return
    matrix_objs[matrix_name] = matrix
    try:
        with open(file_name, "w") as file:
            json.dump(matrix_objs, file, indent=4)
    except:
        print("Couldn't write matrix to file")
        
def overwrite_file(matrices: dict):
    try:
        file = open(file_name, 'w')
        file.write(json.dumps(matrices))
    except:
        print("Couldn't open file")
    finally:
        file.close()

def get_matrices_from_file() -> dict:
    try:
        file = open(file_name, 'r')
        matrix_objs = json.load(file)
    except:
        print("Couldn't open file")
    finally:
        file.close()
    return matrix_objs

def view_whole_file(options: list):
    if len(options) > 0:
        print("'ls' takes no arguments")
        return
    matrix_data = get_matrices_from_file()    
    for matrix_name in matrix_data:
        print_matrix(matrix_data[matrix_name], matrix_name)
# end file stuff

# matrix functions
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
                string_no_comma += "  ]"
        print(string_no_comma)

def parse_matrix(properties: list):
    try:
        rows = int(properties[0])
        string_values = properties[1].split(',')
        if (len(string_values) % rows != 0):
            print("Values needs to be multiple of row_count")
            return
        float_values = []
        for values in string_values:
            float_values.append(float(values))        
    except:
        print("row_count and values need to be numbers")
        return
    return {
        "rows"    : rows,
        "columns" : int(len(float_values)/rows),
        "values"  : float_values
    }
    
def get_matrix_index(mult: int, const: int, add: int) -> int:
    return mult * const + add

def multiply_matrix(options: list):
    if len(options) < 2:
        print("provide the name of 2 matrices")
        return
    add_mat_to_file = False
    if len(options) == 3:
        if options[2] != "w":
            print("use the 'w' option to add matrix to the file after calculation")
            return
        add_mat_to_file = True
    matrix_objs = get_matrices_from_file()
    mat1_name = options[0]
    mat2_name = options[1]
    mat1 = matrix_objs.get(mat1_name, None)
    if not mat1:
        return
    mat2 = matrix_objs.get(mat2_name, None)
    if not mat2:
        return 
    if mat1["columns"] != mat2["rows"]:
        print("matrices have incompatible dimensions")
        return
    new_mat = multiply(mat1, mat2)
    # print(matrix_array[0])
    new_mat_name = f"{mat1_name}*{mat2_name}"
    if add_mat_to_file:
        add_to_file(new_mat, new_mat_name)
        print("matrix added to file")
    print_matrix(new_mat, new_mat_name)
    
def multiply(matrix1: dict, matrix2: dict) -> dict:
    matrix_array  = []
    mat1_rows = matrix1["rows"]
    mat2_columns = matrix2["columns"]
    mat1_columns = matrix1["columns"]
    for matrix_count in range(0, mat1_columns):
        temp_matrix = []
        for values in range(0, mat1_rows * mat2_columns):
            temp_matrix.append(values)
        for b in range(0, mat1_rows):
            for c in range(0, mat2_columns):
                temp_matrix[get_matrix_index(b, mat2_columns, c)] = matrix1["values"][get_matrix_index(b, mat1_columns, matrix_count)] * matrix2["values"][get_matrix_index(matrix_count, mat2_columns, c)]
        matrix_array.append(temp_matrix)
    for thing2 in range(0, len(matrix_array) - 1):
        for thing in range(0, len(matrix_array[0])):
            matrix_array[0][thing] += matrix_array[thing2 + 1][thing]
    return {   
        "rows"    : mat1_rows,
        "columns" : mat2_columns,
        "values"  : matrix_array[0]
    }
    

def add_matrix(options: list, scale: int=1):
    if len(options) < 2:
        print("provide the name of two matrices")
        return
    write = False
    if len(options) == 3:
        if options[2] != "w":
            print("use w option to write to file")
        write = True
    scale = 1 if scale > -1 else scale
    scale = -1 if scale < -1 else scale
    matrix_data = get_matrices_from_file()
    matrix_name_1 = options[0]
    matrix_name_2 = options[1]
    matrix_obj_1 = matrix_data.get(matrix_name_1, None)
    matrix_obj_2 = matrix_data.get(matrix_name_2, None)
    found_both = True
    if not matrix_obj_1:
        print(f"couldn't find matrix {matrix_name_1}")
        found_both = False
    if not matrix_obj_2:
        print(f"couldn't find matrix {matrix_name_2}")
        found_both = False
        
    if not found_both:
        return
    
    matrix_1_rows = matrix_obj_1["rows"]
    matrix_2_rows = matrix_obj_2["rows"]
    matrix_1_values = matrix_obj_1["values"]
    matrix_2_values = matrix_obj_2["values"]
    if matrix_1_rows != matrix_2_rows or len(matrix_1_values) != len(matrix_2_values):
        print(f"{matrix_name_1} and {matrix_name_2} have incompatible dimensions")
        return
    join_string = "+"
    if scale == -1:
        join_string = "-"
    new_matrix_name = matrix_name_1 + join_string + matrix_name_2
    values = []
    
    for matrix_idx in range(0, len(matrix_1_values)):
        values.append(matrix_1_values[matrix_idx] + scale * matrix_2_values[matrix_idx])
    
    new_matrix = {
        "rows"   : matrix_1_rows,
        "columns" : int(len(values)/matrix_1_rows),
        "values" : values
    }
    if write:
        add_to_file(new_matrix, new_matrix_name)
    print_matrix(new_matrix, new_matrix_name)

def subtract_matrix(options: list):
    add_matrix(options, -1)

def scale_matrix(options: list):
    if len(options) < 2:
        print("Provide a matrix name and a scalar value")
        return
    write = False
    if len(options) == 3:
        if options[2] != "w":
            print("use w option to write to file")
        write = True

    matrix_data = get_matrices_from_file()
    if not matrix_data:
        return
    matrix_name = options[0]
    matrix_obj = matrix_data.get(matrix_name, None)
    if not matrix_obj:
        print(f"couldn't find matrix {matrix_name}")
        return
    scale = 0
    try:
        scale = float(options[1])
    except:
        print("couldn't convert option 2 to a float")
        return
    for value_idx in range(0, len(matrix_obj["values"])):
        matrix_obj["values"][value_idx] *= scale
    new_matrix_name = matrix_name + "s"
    if write:
        add_to_file(matrix_obj, new_matrix_name)
    print_matrix(matrix_obj, new_matrix_name)

def transpose_matrix(options: list):
    if len(options) < 1:
        print("Provide the name of the matrix to transpose")
        return
    write = False
    if len(options) == 2:
        if options[1] == 'w':
            write = True
    matrix_objs = get_matrices_from_file()
    if not matrix_objs:
        return
    mat_to_transpose = matrix_objs.get(options[0], None)
    if not mat_to_transpose:
        return
    new_list = transpose(mat_to_transpose["values"], mat_to_transpose["columns"], mat_to_transpose["rows"])
    write_mat = {
    "rows"    : mat_to_transpose["columns"],
    "columns" : mat_to_transpose["rows"],
    "values"  : new_list
    }
    trans_mat_name = options[0] + "t"
    if write:
        add_to_file(write_mat, trans_mat_name)
    print_matrix(write_mat, trans_mat_name)

def transpose(matrix: list, columns: int, rows: int) -> list:
    new_list = []
    for column in range(0, columns):
        for row in range(0, rows):
            new_list.append(matrix[get_matrix_index(row, columns, column)])
    return new_list

def find_determinate(options: list):
    if len(options) < 1:
        print("Provide the name of the matrix to find the determinate of")
        return
    matrix_objs = get_matrices_from_file()
    if not matrix_objs:
        print("Couldn't get matrices")
        return
    matrix_to_det = matrix_objs.get(options[0], None)
    if not matrix_to_det:
        print("couldnt matrix")
        return
    mat_rows = matrix_to_det["rows"]
    mat_cols = matrix_to_det["columns"]
    if mat_rows != mat_cols:
        print("Cant find determinate of non perfect square matrices")
        return
    print(determinate_calculation(matrix_to_det["values"], mat_rows))
    

def determinate_calculation(matrix: list, side: int):
    if(side == 1):
        return matrix[0]
    value = 0
    
    for column in range(0, side):
        matrix_to_det = []
        for row in range(1, side):
            for extra in range(0, side):
                determin_append = get_matrix_index(row, side, extra)
                if determin_append != get_matrix_index(row, side, column):
                    matrix_to_det.append(matrix[determin_append])
        value += pow(-1, column) * matrix[column] * determinate_calculation(matrix_to_det, side - 1)
    return value

def find_inverse(options: list):
    if len(options) < 1:
        print("Provide the name of the matrix to find the inverse of")
        return
    matrix_objs = get_matrices_from_file()
    if not matrix_objs:
        print("couldn't matrix")
        return
    matrix_to_inv = matrix_objs.get(options[0], None)
    if not matrix_to_inv:
        print("couldn't matrix")
        return
    mat_rows = matrix_to_inv["rows"]
    mat_columns = matrix_to_inv["columns"]
    if mat_rows != mat_columns:
        print("Can't find the inverse of non perfect square matrices")
        return
    
    inverse_calculation(matrix_to_inv["values"], matrix_to_inv["rows"])

def inverse_calculation(matrix: list, side: int):
    determinate = determinate_calculation(matrix, side)
    if determinate == 0:
        print("Determinate is 0 -> The matrix is singular")
        return
    mat_to_return = []
    for matrix_pos in range(0, len(matrix)):
        mat_to_return.append(0)
        mat_to_det = []
        exponent_list = []
        for a in range(0, side):
            for b in range(0, side):
                idx = get_matrix_index(a, side, b)
                idx_mod = idx % side
                idx_div = int(idx / side)
                if idx_mod != matrix_pos % side and idx_div != int(matrix_pos / side):
                    mat_to_det.append(matrix[idx])
                exponent_list.append(a+b)
        cofactor = pow(-1, exponent_list[matrix_pos]) * determinate_calculation(mat_to_det, side - 1)
        mat_to_return[matrix_pos] = cofactor
    print("\nCofactor matrix")
    prettify_matrix(mat_to_return, side)
    mat_to_return = transpose(mat_to_return, side, side)
    print("\nTranspose matrix")
    prettify_matrix(mat_to_return, side)
    print(f"\ndeterminate - {determinate}\n")
    print(f"\nInverse matrix -> matrix/{determinate}")
    inverse_determinate = 1/determinate
    for number in range(0, len(mat_to_return)):
        mat_to_return[number] *= inverse_determinate
    prettify_matrix(mat_to_return, side)

def back_failsafe(options: list=None):
    return True

def mat_help(options: list=None):
    print("-" * 55)
    for command in ex_commands:
        print(f"\n{command} " + " " * (7 - len(command)) + f"- {ex_commands_help[command]}")
    print("\n" + "-" * 55)

def my_exit(options: list=None):
    exit()

ex_commands = {
    "x"     : my_exit,
    "exit"  : my_exit,
    "back"  : back_failsafe,
    "help"  : mat_help,
    "ls"    : view_whole_file,
    "mult"  : multiply_matrix,
    "add"   : add_matrix,
    "sub"   : subtract_matrix,
    "scale" : scale_matrix,
    "deter" : find_determinate,
    "trans" : transpose_matrix,
    "inv"   : find_inverse
}

ex_commands_help = {
    "x"     : "exits the application",
    "exit"  : "exits the application",
    "back"  : "go back one menu",
    "help"  : "displays this list of command descriptions",
    "ls"    : "view all matrices in the file",
    "mult"  : "multiply two matrices together",
    "add"   : "add two matrices together",
    "sub"   : "subtract two matrices together",
    "scale" : "scale matrix by coefficient",
    "deter" : "find determinate of matrix",
    "trans" : "transpose matrix",
    "inv"   : "find inverse of matrix"
}
# End matrix functions

def execute(options: list):
    while True:
        user_input = input("matrixinator> ").lower()
        user_input = user_input.split(" ")
        user_command = user_input[0]
        
        if "default" in user_input:
            print("Can't use the default matrix")
            continue
        
        back = False
        
        if user_command not in ex_commands:
            print("not a matrix operation")
            return
        back = ex_commands[user_command](user_input[1:])
        if back:
            return

# Database functions
def add(options: list):
    if len(options) != 3:
        print("Provide name row_count and values\nExample, add matrix1 2 1,2,3,4")
        return
    matrix_parsed = parse_matrix(options[1:])
    if not matrix_parsed:
        return
    matrix_add = matrix_parsed
    add_to_file(matrix_add, options[0])
    print(f"\nMatrix {options[0]} was added")
    print_matrix(matrix_parsed, options[0])

def remove(options: list):
    if len(options) != 1:
        print("Provide the name of matrix to remove\nExample, rm matrix1")
        return
    matrix_data = get_matrices_from_file()
    if not matrix_data:
        return
    if matrix_data.pop(options[0], None):
        print(f"Matrix {options[0]} was removed")
    else:
        print("No matrix exists with that name")
        return
    overwrite_file(matrix_data)

def search(options: list):
    if len(options) != 1:
        print("Provide the name of the matrix you are searching for\nExample, search matrix1")
        return
    matrix_data = get_matrices_from_file()
    if not matrix_data:
        return
    matrix_name = options[0]
    if matrix_data.get(matrix_name, None):
        print_matrix(matrix_data[matrix_name], matrix_name)
    else:
        print("matrix not found in file")

def update(options: list):
    if len(options) != 3:
        print("provide name row_count and values\nExample, update matrix1 2 1,2")
        return
    matrix_name = options[0]
    matrix_data = get_matrices_from_file()
    if not matrix_data:
        return
    if not matrix_data.get(matrix_name, None):
        print("no matrix with that name")
        return
    matrix_parsed = parse_matrix(options[1:])
    if not matrix_parsed:
        return
    matrix_data[matrix_name] = matrix_parsed
    overwrite_file(matrix_data)
    print(f"\nMatrix {matrix_name} was updated")
    print_matrix(matrix_parsed, matrix_name)

def help(options: list):
    print("-" * 55)
    for command in commands:
        print(f"\n{command} " + " " * (7 - len(command)) + f"- {commands_help[command]}")
    print("\n" + "-" * 55)

commands = {
    "x"      : my_exit,
    "exit"   : my_exit,
    "help"   : help,
    "add"    : add,
    "rm"     : remove,
    "search" : search,
    "update" : update,
    "ls"     : view_whole_file,
    "mat"    : execute
}

commands_help = {
    "x"      : "exits the application",
    "exit"   : "exits the application",
    "help"   : "displays this list of command descriptions",
    "add"    : "add a matrix to the file",
    "rm"     : "remove a matrix from the file",
    "search" : "search for a matrix name in the file",
    "update" : "update an existing matrix",
    "ls"     : "view all matrices in the file",
    "mat"    : "access the matrix calculator"
}
# End database functions


def start():
    global file_name
    file = None
    try:
        file = open(file_name)
    except:
        file = open(file_name, 'w')
        global empty_file_matrix
        default_matrix = empty_file_matrix
        matrix_string = json.dumps(default_matrix)
        file.write(matrix_string)
    file.close()
    while True:
        user_input = input("main> ").lower()
        
        user_input = user_input.split(" ")
        user_command = user_input[0]
        
        if "default" in user_input:
            print("Can't use the default matrix")
            continue
        
        if user_command not in commands:
            print("Not a command use 'help' to see a list of all commands")
            continue
        commands[user_input[0]](user_input[1:])

start()
