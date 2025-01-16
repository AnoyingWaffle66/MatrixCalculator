import json

# "database" file name
file_name = "matrix.txt"
empty_file_matrix = {}

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
            print(f"{matrix_sub} " + " " * (7 - len(matrix_sub)) + f"- {matrix[matrix_sub]}")
    print("")

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
    mat1 = matrix_objs.get(options[0], None)
    if not mat1:
        return
    mat2 = matrix_objs.get(options[1], None)
    if not mat2:
        return 
    if mat1["columns"] != mat2["rows"]:
        print("matrices have incompatible dimensions")
        return
    first_new_values  = []
    second_new_values = []
    for first in range(0, len(mat1["values"])):
        for second in range(0, mat2["columns"]):
            if(first % 2) == 0:
                first_new_values.append(mat1["values"][first] * mat2["values"][second])
            else:
                second_new_values.append(mat1["values"][first] * mat2["values"][mat2["columns"] + second])
    for add_idx in range(0, len(first_new_values)):
        first_new_values[add_idx] += second_new_values[add_idx]
    new_mat = {
        "rows"    : mat1["rows"],
        "columns" : mat2["columns"],
        "values"  : first_new_values
    }
    if add_mat_to_file:
        add_to_file(new_mat, f"{options[0]}_*_{options[1]}")
        print("matrix added to file")
    print(first_new_values)

def add_matrix(options: list, scale: int=1):
    if len(options) != 2:
        print("provide the name of two matrices")
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
    new_matrix = {
        new_matrix_name : {
            "rows"   : matrix_1_rows,
            "values" : []
        }
    }
    
    for matrix_idx in range(0, len(matrix_1_values)):
        new_matrix[new_matrix_name]["values"].append(matrix_1_values[matrix_idx] + scale * matrix_2_values[matrix_idx])
    print_matrix(new_matrix[new_matrix_name], new_matrix_name)

def subtract_matrix(options: list):
    add_matrix(options, -1)

def scale_matrix(options: list):
    if len(options) != 2:
        print("Provide a matrix name and a scalar value")
        return

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
    print_matrix(matrix_obj, matrix_name)

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
    new_list = []
    for column in range(0, mat_to_transpose["columns"]):
        for row in range(0, mat_to_transpose["rows"]):
            new_list.append(mat_to_transpose["values"][column + row*mat_to_transpose["columns"]])
            pass
    write_mat = {
    "rows"    : mat_to_transpose["columns"],
    "columns" : mat_to_transpose["rows"],
    "values"  : new_list
    }
    trans_mat_name = options[0] + "t"
    if write:
        add_to_file(write_mat, trans_mat_name)
    print_matrix(write_mat, trans_mat_name)

def find_determinate(options: list):
    if len(options) != 1:
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
                determin_append = row * side + extra
                if determin_append != row * side + column:
                    matrix_to_det.append(matrix[determin_append])
        value += pow(-1, column) * matrix[column] * determinate_calculation(matrix_to_det, side - 1)
    return value

def back_failsafe(options: list=None):
    return True

def mat_help(options: list=None):
    print("-" * 55)
    for command in ex_commands:
        print(f"\n{command} " + " " * (7 - len(command)) + f"- {ex_commands_help[command]}")
    print("\n" + "-" * 55)

ex_commands = {
    "x"     : exit,
    "exit"  : exit,
    "back"  : back_failsafe,
    "help"  : mat_help,
    "ls"    : view_whole_file,
    "mult"  : multiply_matrix,
    "add"   : add_matrix,
    "sub"   : subtract_matrix,
    "scale" : scale_matrix,
    "deter" : find_determinate,
    "trans" : transpose_matrix
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
    "trans" : "transpose matrix"
}
# End matrix functions

def execute(options: list):
    while True:
        user_input = input("matrixinator> ").lower()
        user_input = user_input.split(" ")
        if user_input[0] not in ex_commands:
            print("not a matrix operation")
        elif(user_input[0] == "exit" or user_input[0] == "x"):
            ex_commands[user_input[0]]()
        else:
            thing = ex_commands[user_input[0]](user_input[1:])
        if thing:
            return

# Database functions
def add(options: list):
    if len(options) != 3:
        print("Not enough arguments, provide - name row_count values\nExample, add matrix1 2 1,2,3,4")
        return
    matrix_parsed = parse_matrix(options[1:])
    if not matrix_parsed:
        return
    matrix_add = matrix_parsed
    add_to_file(matrix_add, options[0])

def remove(options: list):
    if len(options) != 1:
        print("Provide one name of matrix to remove")
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
        print("Provide the name of the matrix you are searching for")
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
        print("provide all necessary parameters")
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

def help(options: list):
    print("-" * 55)
    for command in commands:
        print(f"\n{command} " + " " * (7 - len(command)) + f"- {commands_help[command]}")
    print("\n" + "-" * 55)

commands = {
    "x"      : exit,
    "exit"   : exit,
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
        
        if user_input[0] not in commands:
            print("Not a command use 'help' to see a list of all commands")
        elif (user_input[0] == "exit" or user_input[0] == "x"):
            exit()
        else:
            commands[user_input[0]](user_input[1:])

start()
