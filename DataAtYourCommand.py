import json

# "database" file name
file_name = "matrix.txt"
empty_file_matrix = {}

# matrix functions
def print_matrix(matrix: dict, matrix_name: str):
    print("")
    print(f"name   - {matrix_name}")
    for matrix_sub in matrix:
            print(f"{matrix_sub} " + " " * (6 - len(matrix_sub)) + f"- {matrix[matrix_sub]}")
    print("")

def multiply_matrix(options: list):
    print("Multiply matrix")

def add_matrix(options: list):
    print("add matrix")

def subtract_matrix(options: list):
    print("subtract matrix")

def scale_matrix(options: list):
    if len(options) != 2:
        print("Provide a matrix name and a scalar value")
        return
    file = None
    matrix_data = None
    try:
        file = open(file_name, 'r')
        matrix_data = json.load(file)
        file.close()
    except:
        print("couldn't open file")
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
    print("transpose matrix")

def find_determinate(options: list):
    print("find matrix")

def back_failsafe(options: list=None):
    return True

def mat_help(options: list=None):
    print("-" * 55)
    for command in ex_commands:
        print(f"\n{command} " + " " * (6 - len(command)) + f"- {ex_commands_help[command]}")
    print("\n" + "-" * 55)

def view_whole_file(options: list):
    if len(options) > 0:
        print("'ls' takes no arguments")
        return
    matrix_data = None
    file = None
    try:
        file = open(file_name, 'r')
        matrix_data = json.load(file)
    except:
        pass
    finally:
        file.close()
        
    for matrix_name in matrix_data:
        print_matrix(matrix_data[matrix_name], matrix_name)
    
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
    print("execute")
    while True:
        user_input = input("matrixinator>").lower()
        
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
    
    rows = 1
    float_values = []
    try:
        rows = int(options[1])
        string_values = options[2].split(',')
        if (len(string_values) % rows != 0):
            print("Values needs to be multiple of row_count")
            return
        for values in string_values:
            float_values.append(float(values))        
    except:
        print("row_count and values need to be numbers")
    
    file = None
    matrix_data = None
    try:
        file = open(file_name, 'r')
        matrix_data = json.load(file)
        matrix_data[options[0]] = {
            "rows" : rows,
            "values" : float_values
        }
        file.close()
    except:
        print(f"Couldn't open file: {file_name}")
    
    global empty_file_matrix
    try:
        with open(file_name, 'w') as file:
            json.dump(matrix_data, file, indent=4)
    except json.JSONDecodeError:
        print("Couldn't dump matrix into file. Dumping default in.")
        file.close()
        with open(file_name, 'w') as file:
            file.write(json.dumps(empty_file_matrix))        

def remove(options: list):
    if len(options) != 1:
        print("Provide one name of matrix to remove")
        return
    try:
        file = open(file_name, 'r+')
        matrix_data = json.load(file)
        if matrix_data.pop(options[0], None):
            print(f"Matrix {options[0]} was removed")
        else:
            print("No matrix exists with that name")
        file.close()
        file = open(file_name, 'w')
        file.write(json.dumps(matrix_data))
        file.close()
    except:
        print("something went wrong")

def search(options: list):
    if len(options) != 1:
        print("Provide the name of the matrix you are searching for")
        return
    try:
        file = open(file_name, 'r')
        matrix_data = json.load(file)
        if matrix_data.get(options[0], None):
            print(f"\n{options[0]}")
            for matrix_sub in matrix_data[options[0]]:
                print(f"{matrix_sub} - {matrix_data[options[0]][matrix_sub]}")
        else:
            print("matrix not found in file")
    except:
        print("Couldn't open file")

def update(options: list):
    if len(options) != 3:
        print("provide all necessary parameters")
        return
    file = None
    matrix_data = None
    try:
        file = open(file_name, 'r')
        matrix_data = json.load(file)
        if not matrix_data.get(options[0], None):
            print("no matrix with that name")
            return        
        try:
            rows = 1
            float_values = []
            rows = int(options[1])
            string_values = options[2].split(',')
            if (len(string_values) % rows != 0):
                print("Values needs to be multiple of row_count")
                return
            for values in string_values:
                float_values.append(float(values)) 
            matrix_data[options[0]] = {
                "rows" : rows,
                "values" : float_values
            }
        except:
            print("numbers required")
        file.close()
    except:
        print("couldnt open file1")
    finally:
        file.close()
    try:
        with open(file_name, 'w') as file:
            json.dump(matrix_data, file, indent=4)
    except:
        file.close()
        print("couldn't open file2")

def help(options: list):
    print("-" * 55)
    for command in commands:
        print(f"\n{command} " + " " * (6 - len(command)) + f"- {commands_help[command]}")
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
