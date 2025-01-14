import json

# "database" file name
file_name = "matrix.txt"

# matrix functions
def multiply_matrix(options: list):
    print("Multiply matrix")

def add_matrix(options: list):
    print("add matrix")

def subtract_matrix(options: list):
    print("subtract matrix")

def scale_matrix(options: list):
    print("scale matrix")

def transpose_matrix(options: list):
    print("transpose matrix")

def find_determinate(options: list):
    print("find matrix")

def back_failsafe(options: list=None):
    return True

ex_commands = {
    "x"     : exit,
    "exit"  : exit,
    "back"  : back_failsafe,
    "mult"  : multiply_matrix,
    "add"   : add_matrix,
    "sub"   : subtract_matrix,
    "scale" : scale_matrix,
    "deter" : find_determinate,
    "trans" : transpose_matrix
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
def view_whole_file(options: list):
    print("view whole file")

def add(options: list):
    if len(options) != 3:
        print("Not enough arguments, provide - name row_count values\nExample, add matrix1 2 1,2,3,4")
        return
    try:
        rows = float(options[1])
        string_values = options[2].split(',')
        if (len(string_values) % rows != 0):
            print("Values needs to be multiple of row_count")
        float_values = []
        for values in string_values:
            float_values.append(float(values))
        print("appended values")
        with open(file_name, "r") as file:
            print("starting file read")
            thing = file.read()
            print("file read")
            data = json.load(thing)
            print("file read finished")
        print("load worked")
        new_matrix = {
            "name"   : options[0],
            "rows"   : rows,
            "values" : float_values
            }
        
        new_matrix = json.dumps(new_matrix)
        new_matrix += ","
        data += new_matrix
        
        with open(file_name, 'w') as file:
            json.dumps(data, file, indent=4)
            print("data dumped")
    except:
        print("row_count and values need to be numbers")
        file.close()

def remove(options: list):
    print("remove")

def search(options: list):
    print("search")

def update(options: list):
    print("update")

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
    "all"    : view_whole_file,
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
    "all"    : "view all matrices in the file",
    "mat"    : "access the matrix calculator"
}
# End database functions


def start():
    global file_name
    file = None
    try:
        file = open(file_name)
        file.close()
    except:
        file = open(file_name, 'w')
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
