import json
import functional.matrix_functions as mc
import functional.vector_functions as vc
import functional.linear_transformation_matrices as lt
import numpy as np
import print_stuff as pm

# "database" file name
matrix_file = "jsons/m.json"
vector_file = "jsons/v.json"

# "database" file name no .json

empty_file_matrix = {
    "default" : {
        "rows" : 0,
        "columns" : 0,
        "Values" : []
    }
}

empty_file_vector = {
    "default" : {
        "values" : []
    }
}

# file stuff
def add_to_file(file_name: str, object: dict, object_name: str):
    matrix_objs = get_matrices_dict(file_name)
    if not matrix_objs:
        print("OH NO IS BROKEN")
        return
    matrix_objs[object_name] = object
    try:
        with open(file_name, "w") as file:
            json.dump(matrix_objs, file, indent=4)
    except:
        print("Couldn't write matrix to file")

def overwrite_file(file_name: str, objects: dict):
    try:
        file = open(file_name, 'w')
        file.write(json.dumps(objects))
    except:
        print("Couldn't open file")
    finally:
        file.close()

def get_matrices_dict(file_name: str) -> dict:
    matrix_objs = None
    try:
        with open(file_name, 'r') as file:
            matrix_objs = json.load(file)
    except:
        print("Couldn't open file")
    return matrix_objs

def get_matrices_list(matrices: list) -> list:
    global matrix_file
    return_list = []
    matrix_objs = get_matrices_dict(matrix_file)
    if not matrix_objs:
        return None
    for matrix in matrices:
        mat_to_add = matrix_objs.get(matrix, None)
        if not mat_to_add:
            print("Couldn't find matrix")
            return None
        return_list.append(mat_to_add)
    return return_list

def get_vec_list(vectors: list) -> list:
    global vector_file
    return_list = []
    vec_objs = get_matrices_dict(vector_file)
    if not vec_objs:
        return None
    for vector in vectors:
        vec_to_add = vec_objs.get(vector, None)
        if not vec_to_add:
            print("Couldn't find vector")
            return None
        return_list.append(vec_to_add)
    return return_list

def view_all_vectors(options: list):
    view_whole_file(["v"])

def view_all_matrix(options: list):
    view_whole_file(["m"])

def view_whole_file(options: list):
    if len(options) != 1:
        print("'ls' needs a file name to view from main")
        return
    file_to_get = "jsons/" + options[0] + ".json"
    match file_to_get:
        case "jsons/m.json":
            matrix_data = get_matrices_dict(file_to_get)
            for matrix_name in matrix_data:
                pm.print_matrix(matrix_data[matrix_name], matrix_name)
        case "jsons/v.json":
            vec_data = get_matrices_dict(file_to_get)
            for vec_name in vec_data:
                pm.print_vector(vec_data[vec_name], vec_name)
            pass
        case _:
            print("Not a file")
            return
# end file stuff

# matrix functions

def parse_matrix(properties: list) -> dict:
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

def value_append(values: list, value: int, string_values: str, attempts: int):
    idx = value
    try:
        for idx in range(value, len(string_values)):
            if "root" in string_values[idx]:
                values.append(np.sqrt(float(string_values[idx][4:])))
            else:
                values.append(float(string_values[idx]))
    except:
        print("values need to numbers and seperated by commas")
        attempts += 1
    return values, attempts


def parse_vector(properties: list) -> dict:
    string_values = properties[0].split(',')
    values = []
    attempts = 0
    while len(values) != len(string_values) and attempts < 1:
        values, attempts = value_append(values, len(values), string_values, attempts)
    if attempts == 1:
        return None
    else:
        return {
            "values" : values
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
    matrix_objs = get_matrices_list(options[0:2])
    if not matrix_objs:
        return
    mat1_name = options[0]
    mat2_name = options[1]
    mat1 = matrix_objs[0]
    mat2 = matrix_objs[1]
    if mat1["columns"] != mat2["rows"]:
        print("matrices have incompatible dimensions")
        return
    new_mat = {
        "rows"    : mat1["rows"],
        "columns" : mat2["columns"],
        "values"  : mc.multiply(mat1["values"], mat2["values"], mat1["columns"], mat1["rows"], mat2["columns"])
    }
    new_mat_name = f"{mat1_name}*{mat2_name}"
    if add_mat_to_file:
        add_to_file(new_mat, new_mat_name)
        print("matrix added to file")
    pm.print_matrix(new_mat, new_mat_name)

def inv_solve(options: list):
    if len(options) < 2:
        print("please provide name of matrix and solution matrix")
        return
    matrix_data = get_matrices_list([options[0]])
    if not matrix_data:
        return
    mat1 = matrix_data[0]
    side = mat1["columns"]
    mat_unparsed = [
        f"{side}",
        options[1]
    ]
    mat2 = parse_matrix(mat_unparsed)
    if not mat2:
        return
    if side != mat2["rows"]:
        return
    is_singular = mc.deter(mat1["values"], side)
    if is_singular == 0:
        print("Determinate is 0, matrix has no inverse")
        return
    write_mat = {
        "rows"    : side,
        "columns" : 1,
        "values"  : mc.solve(mat1["values"], mat2["values"], side)
    }
    pm.print_matrix(write_mat, f"{options[0]}solve")

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
    mat_data = get_matrices_list(options[0:])
    if not mat_data:
        return
    mat1_name   = options[0]
    mat2_name   = options[1]
    mat1        = mat_data[0]
    mat2        = mat_data[1]
    mat1_rows   = mat1["rows"]
    mat2_rows   = mat2["rows"]
    mat1_values = mat1["values"]
    mat2_values = mat2["values"]
    
    if mat1_rows != mat2_rows or len(mat1_values) != len(mat2_values):
        print(f"{mat1_name} and {mat2_name} have incompatible dimensions")
        return
    join_string = "+"
    if scale == -1:
        join_string = "-"
    new_matrix_name = mat1_name + join_string + mat2_name
    new_matrix = {
        "rows"    : mat1_rows,
        "columns" : int(len(mat1_values)/mat1_rows),
        "values"  : mc.add(mat1_values, mat2_values)
    }
    if write:
        add_to_file(new_matrix, new_matrix_name)
    pm.print_matrix(new_matrix, new_matrix_name)

def subtract_matrix(options: list):
    if len(options) < 2:
        print("more options")
        return
    mats = get_matrices_list(options[0:])
    if not mats:
        return
    mat1 = mats[0]
    mat2 = mats[1]
    if mat1["rows"] != mat2["rows"]:
        print("matrices have incompatible dimensions")
        return
    print(pm.prettify_matrix(mc.subtract(mat1["values"], mat2["values"]), mat1["rows"]))

def scale_matrix(options: list):
    if len(options) < 2:
        print("Provide a matrix name and a scalar value")
        return
    write = False
    if len(options) == 3:
        if options[2] != "w":
            print("use w option to write to file")
        write = True

    matrix_obj = get_matrices_list([options[0]])
    if not matrix_obj:
        return
    mat_name = options[0]
    try:
        scale = float(options[1])
    except:
        print("couldn't convert option 2 to a float")
        return
    matrix_obj[0]["values"] = mc.scale(matrix_obj[0]["values"], scale)
    new_matrix_name = mat_name + "s"
    if write:
        add_to_file(matrix_obj[0], new_matrix_name)
    pm.print_matrix(matrix_obj[0], new_matrix_name)

def transpose_matrix(options: list):
    if len(options) < 1:
        print("Provide the name of the matrix to transpose")
        return
    write = False
    if len(options) == 2:
        if options[1] == 'w':
            write = True
    mat_to_transpose = get_matrices_list([options[0]])
    if not mat_to_transpose:
        return
    new_list = mc.transpose(mat_to_transpose[0]["values"], mat_to_transpose[0]["columns"], mat_to_transpose[0]["rows"])
    write_mat = {
    "rows"    : mat_to_transpose[0]["columns"],
    "columns" : mat_to_transpose[0]["rows"],
    "values"  : new_list
    }
    trans_mat_name = options[0] + "t"
    if write:
        add_to_file(write_mat, trans_mat_name)
    pm.print_matrix(write_mat, trans_mat_name)

def find_determinate(options: list):
    if len(options) < 1:
        print("Provide the name of the matrix to find the determinate of")
        return
    matrix_to_det = get_matrices_list([options[0]])
    if not matrix_to_det:
        return
    mat_rows = matrix_to_det[0]["rows"]
    mat_cols = matrix_to_det[0]["columns"]
    if mat_rows != mat_cols:
        print("Cant find determinate of non perfect square matrices")
        return
    print(mc.deter(matrix_to_det[0]["values"], mat_rows))
    

def find_inverse(options: list):
    if len(options) < 1:
        print("Provide the name of the matrix to find the inverse of")
        return
    matrix_to_inv = get_matrices_list([options[0]])
    if not matrix_to_inv:
        return
    mat_rows = matrix_to_inv[0]["rows"]
    mat_columns = matrix_to_inv[0]["columns"]
    if mat_rows != mat_columns:
        print("Can't find the inverse of non perfect square matrices")
        return
    write_mat = {
        "rows"    : mat_rows,
        "columns" : mat_columns,
        "values"  : mc.inverse(matrix_to_inv[0]["values"], mat_rows)
    }
    pm.print_matrix(write_mat, f"{options[0]}inv")

def clear_mats(options: list=None):
    global matrix_file
    global empty_file_matrix
    overwrite_file(matrix_file, empty_file_matrix)
    print("All matrices have been cleared")

def back_failsafe(options: list=None):
    return True

def add_mat_to_file(options: list):
    if len(options) < 3:
        print("provide name rows and values of matrix")
        return
    add(["m", options[0], options[1], options[2]])

def remove_mat_from_file(options: list):
    if len(options) < 1:
        print("provide the name of the matrix to remove")
        return
    remove(["m", options[0]])

def mat_help(options: list=None):
    print("-" * 55)
    for command in mat_commands:
        print(f"\n{command} " + " " * (7 - len(command)) + f"- {mat_commands_help[command]}")
    print("\n" + "-" * 55)

def my_exit(options: list=None):
    exit()

mat_commands = {
    "x"     : my_exit,
    "back"  : back_failsafe,
    "help"  : mat_help,
    "ls"    : view_all_matrix,
    "clear" : clear_mats,
    "add"   : add_mat_to_file,
    "rm"    : remove_mat_from_file,
    "plus"  : add_matrix,
    "sub"   : subtract_matrix,
    "mult"  : multiply_matrix,
    "scale" : scale_matrix,
    "trans" : transpose_matrix,
    "deter" : find_determinate,
    "inv"   : find_inverse,
    "solve" : inv_solve,
}

mat_commands_help = {
    "x"     : "exits the application",
    "back"  : "go back one menu",
    "help"  : "displays this list of command descriptions",
    "ls"    : "view all matrices in the file",
    "clear" : "clear all matrices in the file",
    "add"   : "add matrix to file",
    "rm"    : "remove matrix from file",
    "plus"  : "add two matrices together",
    "sub"   : "subtract two matrices from each other",
    "mult"  : "multiply two matrices together",
    "scale" : "scale matrix by coefficient",
    "trans" : "transpose matrix",
    "deter" : "find determinate of matrix",
    "inv"   : "find inverse of matrix",
    "solve" : "solve a system equations using inverse matrix",
}
# End matrix functions

def matrix(options: list):
    global matrix_file
    try:
        file = open(matrix_file)
    except:
        file = open(matrix_file, 'w')
        global empty_file_matrix
        matrix_string = json.dumps(empty_file_matrix)
        file.write(matrix_string)
    file.close()
    while True:
        user_input = input("matrixinator> ").lower()
        user_input = user_input.split(" ")
        user_command = user_input[0]
        
        if "default" in user_input:
            print("Can't use the default matrix")
            continue
        
        back = False
        
        if user_command not in mat_commands:
            print("not a matrix operation")
            continue
        back = mat_commands[user_command](user_input[1:])
        if back:
            return
        
# Start vector functions

def need_one_vec(vec_name: list):
    if len(vec_name) != 1:
        print("Provide the name of one vector")
        return None
    global vector_file
    vector = get_vec_list([vec_name[0]])
    if not vector:
        return None
    return vector[0]["values"]

def need_two_vec(vec_names: list):
    if len(vec_names) != 2:
        print("Provide the name of two vectors")
        return None, None
    global vector_file
    vectors = get_vec_list(vec_names[0:])
    if not vectors:
        return None, None
    if len(vectors[0]["values"]) != len(vectors[1]["values"]):
        print("Vectors need to be the same dimension")
        return None, None
    return vectors[0]["values"], vectors[1]["values"]

def add_vector(options: list):
    vec1, vec2 = need_two_vec(options[0:])
    if not vec1 or not vec2:
        return
    print(pm.prettify_vector(vc.add(vec1, vec2)) + "\n")

def sub_vector(options: list):
    vec1, vec2 = need_two_vec(options[0:])
    if not vec1 or not vec2:
        return
    print(pm.prettify_vector(vc.sub(vec1, vec2)) + "\n")

def magnitude(options: list):
    if len(options) < 1:
        return
    vec1 = need_one_vec(options[0:])
    if not vec1:
        return
    print("%.4f" % vc.mag(vec1))

def dot_product(options: list):
    vec1, vec2 = need_two_vec(options[0:])
    if not vec1 or not vec2:
        return
    print(f"{vc.dot(vec1, vec2)}\n")

def scale_vector(options: list):
    if len(options) < 1:
        return
    vec = need_one_vec([options[0]])
    if not vec:
        return
    try:
        scale = float(options[1])
    except:
        print("Provide a numeric value for a scalar")
    print(pm.prettify_vector(vc.scale(vec, scale)) + "\n")

def distance(options: list):
    vec1, vec2 = need_two_vec(options[0:])
    if not vec1 or not vec2:
        return
    print("%.4f" % vc.distance(vec1, vec2))

def normalize(options: list):
    if len(options) < 1:
        return
    vec = need_one_vec([options[0]])
    if not vec:
        return
    print(pm.prettify_vector(vc.normalize(vec)) + "\n")

def point_in_same_direction(options: list):
    vec1, vec2 = need_two_vec(options[0:])
    if not vec1 or not vec2:
        return
    print(pm.prettify_vector(vc.point(vec1, vec2)) + "\n")
    
def project(options: list):
    vec1, vec2 = need_two_vec(options[0:])
    if not vec1 or not vec2:
        return
    vc.proj(vec1, vec2)
    
def cross(options: list):
    if len(options) < 1:
        return
    vec1 = need_one_vec([options[0]])
    if not vec1:
        return
    if len(vec1) -1 != len(options):
        print("need one less vector than its dimension")
        return
    vecs = []
    for idx in range(len(options)):
        vecs.append(need_one_vec([options[idx]]))
    valid_dimensions = 0
    previous_dimension = 0
    for vec in vecs:
        if previous_dimension == 0:
            previous_dimension = len(vec)
            continue
        valid_dimensions = len(vec)
        if valid_dimensions != previous_dimension:
            print("incompatible dimensions")
            return
        previous_dimension = valid_dimensions
    vc.cross(vecs)

def add_vec_to_file(options: list):
    if len(options) < 2:
        print("provide name and values of vector")
        return
    add(["v", options[0], options[1]])

def remove_vec_from_file(options: list):
    if len(options) < 1:
        print("provide the name of the vector")
        return
    remove(["v", options[0]])

def clear_vecs(options: list=None):
    global vector_file
    global empty_file_vector
    overwrite_file(vector_file, empty_file_vector)
    print("All vectors have been removed")

def vec_help(options: list=None):
    print("-" * 55)
    for command in vec_commands:
        print(f"\n{command} " + " " * (7 - len(command)) + f"- {vec_commands_help[command]}")
    print("\n" + "-" * 55)

vec_commands = {
    "x"     : my_exit,
    "back"  : back_failsafe,
    "help"  : vec_help,
    "ls"    : view_all_vectors,
    "clear" : clear_vecs,
    "add"   : add_vec_to_file,
    "rm"    : remove_vec_from_file,
    "plus"  : add_vector,
    "sub"   : sub_vector,
    "mag"   : magnitude,
    "dot"   : dot_product,
    "scale" : scale_vector,
    "dis"   : distance,
    "norm"  : normalize,
    "point" : point_in_same_direction,
    "proj"  : project,
    "cross" : cross
}

vec_commands_help = {
    "x"     : "exits the application",
    "back"  : "goes back one menu",
    "help"  : "displays this list of commands",
    "ls"    : "view all vectors in file",
    "clear" : "clear all vectors in the file",
    "add"   : "add vector to file",
    "rm"    : "remove vector from file",
    "plus"  : "add two vectors together",
    "sub"   : "subtract two vectors from each other",
    "mag"   : "gets the magnitude of a vector",
    "dot"   : "finds the dot product of two vectors",
    "scale" : "scale a vector by a coefficient",
    "dis"   : "find the distance between two vectors",
    "norm"  : "normalize a vector",
    "point" : "point two vectors in the same direction",
    "proj"  : "project first vector onto second vector",
    "cross" : "finds the cross product of n vectors"
}
# End vector functions

def parse_nums(nums: str) -> list:
    unparsed = nums.split(",")
    parsed = []
    for num in unparsed:
        parsed.append(float(num))
    return parsed

value_no_needed = {
    "rot"         : True,
    "rotx"        : True,
    "roty"        : True,
    "rotz"        : True,
    "rotall"      : True,
    "scale"       : True,
    "scale3"      : True,
    "squishx"     : False,
    "squishy"     : False,
    "squishoutz"  : False,
    "squishouty"  : False,
    "squishoutx"  : False,
    "aboutx"      : False,
    "abouty"      : False,
    "about2"      : True,
    "about3"      : True,
    "skewh"       : True,
    "skewv"       : True,
    "skewx"       : True,
    "skewy"       : True,
    "skewz"       : True
}

transform_strings = {
    "rot"         : "2d rotation",
    "rotx"        : "x rotation in 3d",
    "roty"        : "y rotation in 3d",
    "rotz"        : "z rotation in 3d",
    "rotall"      : "all axis rotation in 3d",
    "scale"       : "2d scale",
    "scale3"      : "3d scale",
    "squishx"     : "orthoganally compress to x axis",
    "squishy"     : "orthoganally compress to y axis",
    "squishoutz"  : "orthoganally compress to x-y plain",
    "squishouty"  : "orthoganally compress to x-z plain",
    "squishoutx"  : "orthoganally compress to y-z plain",
    "aboutx"      : "flip about x, across y",
    "abouty"      : "filp about y, across x",
    "about2"      : "flip about x and y",
    "about3"      : "flip about x, y and z",
    "skewh"       : "horizontal skew",
    "skewv"       : "vertical skew",
    "skewx"       : "x axis skew 3d",
    "skewy"       : "y axis skew 3d",
    "skewz"       : "z axis skew 3d"
}

def catify(options: list):
    mats_to_cat = []
    transforms = []
    length = 2
    for mat_num in range(len(options)):
        transform = options[mat_num]
        if transform not in concats:
            continue
        transforms.append(transform)
        thing = [1.0]
        value_needed = value_no_needed[transform]
        if value_needed:
            thing = parse_nums(options[mat_num + 1])
        if len(thing) == 1:
            thing = thing[0]
        mat_values, length = concats[transform](thing)
        mats_to_cat.append({
                    "rows"    : length,
                    "columns" : length,
                    "values"  : mat_values
                }) 
    identity = []
    if length == 2:
        identity = [1.0, 0.0, 0.0, 1.0]
    elif length == 3:
        identity = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    cat_mat = {
        "rows"    : length,
        "columns" : length,
        "values"  : identity
    }
    mats_to_cat.reverse()
    transforms.reverse()
    for mat in range(len(mats_to_cat)):
        catified = mc.multiply(cat_mat["values"], mats_to_cat[mat]["values"], length, length, length)
        cat_mat["values"] = catified
        print(f"\n{transform_strings[transforms[mat]]}")
        print(pm.prettify_matrix(catified, length))
    global matrix_file
    add_to_file(matrix_file, cat_mat, "cat")

def cat_help(options: list):
    print('-' * 55)
    for command in concats_help:
        print(f"\n{command} " + " " * (9 - len(command)) + f"- {concats_help[command]}")
    print("\n" + '-' * 55)

concats_executable = {
    "x"         : my_exit,
    "back"      : back_failsafe,
    "help"      : cat_help,
    "catify"    : catify
}

concats = {
    "rot"        : lt.rot2,
    "rotx"       : lt.rot3x,
    "roty"       : lt.rot3y,
    "rotz"       : lt.rot3z,
    "rotall"     : lt.rot3all,
    "scale"      : lt.scale2d,
    "scale3"     : lt.scale3d,
    "squishx"    : lt.ortho2x,
    "squishy"    : lt.ortho2y,
    "squishoutz" : lt.ortho3z,
    "squishouty" : lt.ortho3y,
    "squishoutx" : lt.ortho3x,
    "aboutx"     : lt.aboutx,
    "abouty"     : lt.abouty,
    "about2"     : lt.about2d,
    "about3"     : lt.about3d,
    "skewh"      : lt.horizontal_skew,
    "skewv"      : lt.vertical_skew,
    "skewx"      : lt.x_skew,
    "skewy"      : lt.y_skew,
    "skewz"      : lt.z_skew,
}

concats_help = {
    "x"          : "exits the application",    
    "back"       : "goes back one menu",
    "help"       : "displays this list of commands",
    "catify"     : "concatenate multiple matrices through multiplication",
    "rot"        : "rotate in 2d, theta",
    "rotx"       : "rotate around x in 3d, theta",
    "roty"       : "rotate around y in 3d, theta",
    "rotz"       : "rotate around z in 3d, theta",
    "rotall"     : "rotate around all axes in 3d, theta,x,y,z",
    "scale"      : "scale in 2d, x,y",
    "scale3"     : "scale in 3d, x,y,z",
    "squishx"    : "flatten to x axis",
    "squishy"    : "flatten to y axis",
    "squishoutz" : "flatten to x-y plane",
    "squishouty" : "flatten to x-z plane",
    "squishoutx" : "flatten to y-z plane",
    "aboutx"     : "flip across y",
    "abouty"     : "flip across x",
    "about2"     : "flip in 2 dimensions, x,y",
    "about3"     : "flip in 3 dimensions, x,y,z",
    "skewh"      : "skew horizontally, value",
    "skewv"      : "skew vertically, value",
    "skewx"      : "skew the x axis, y,z",
    "skewy"      : "skew the y axis, x,z",
    "skewz"      : "skew the z axis, x,y",
}

def mat_concat(options: list):
    while True:
        user_input = input("concatinator> ").lower()
        
        user_input = user_input.split(" ")
        user_command = user_input[0]
        
        if user_command not in concats_executable:
            print("bad boy")
            continue
        
        back = concats_executable[user_command](user_input[1:])
        if back: 
            return

def vector(options: list):
    global vector_file
    try:
        file = open(vector_file)
    except:
        file = open(vector_file, 'w')
        global empty_file_vector
        vector_string = json.dumps(empty_file_vector)
        file.write(vector_string)
    file.close()
    while True:
        user_input = input("vectorinator> ").lower()
        user_input = user_input.split(" ")
        user_command = user_input[0]
        if "default" in user_input:
            print("Can't use the default vector")
            continue
        
        back = False
        
        if user_command not in vec_commands:
            print("Not a vector operation")
            continue
        back = vec_commands[user_command](user_input[1:])
        if back: 
            return

# Database functions
which_parse = {
    "m" : parse_matrix,
    "v" : parse_vector
}

which_print = {
    "m" : pm.print_matrix,
    "v" : pm.print_vector
}

def add(options: list):
    global matrix_file
    global vector_file
    parsed_thing = None
    file = ""
    match options[0]:
        case "m":
            if len(options[1:]) != 3:
                print("Provide name row_count and values\nExample, add matrix1 2 1,2,3,4")
                return
            file = matrix_file
        case "v":
            if len(options[1:]) != 2:
                print("Provide the name and values for the vector")
                return
            file = vector_file
        case _:
            print("Provide v for vector or m for matrix")
            return
    parsed_thing = which_parse[options[0]](options[2:])
    if not parsed_thing:
        return
    add_to_file(file, parsed_thing, options[1])
    print(f"\n{options[1]} was added")
    which_print[options[0]](parsed_thing, options[1])

def remove(options: list):
    if len(options) != 2:
        print("Incorrect amount or arguments")
        return
    file = ""
    global matrix_file
    global vector_file
    match options[0]:
        case "m":
            file = matrix_file
        case "v":
            file = vector_file
        case _:
            print("Provide m for matrix or v for vector")
            return
    data = get_matrices_dict(file)
    if not data:
        return
    if data.pop(options[1], None):
        print(f"{options[1]} was removed")
    else:
        print("Nothing exists with that name")
        return
    overwrite_file(file, data)

which_clear = {
    "m" : clear_mats,
    "v" : clear_vecs
}

def clear_(options: list):
    if len(options) < 1:
        print("Provide v for vector file or m for matrix file")
        return
    if options[0] not in which_clear:
        print("Provide v for vector file or m for matrix file")
        return
    which_clear[options[0]](options[0:])

def search(options: list):
    if len(options) != 2:
        print("Incorrect amount or arguments")
        return
    file = ""
    global matrix_file
    global vector_file
    match options[0]:
        case "m":
            file = matrix_file
        case "v":
            file = vector_file
        case _:
            print("Provide m for matrix or v for vector")
            return
    data = get_matrices_dict(file)
    if not data:
        return
    matrix_name = options[1]
    if matrix_name not in data:
        print("not in thing")
        return
    which_print[options[0]](data[matrix_name], matrix_name)

def help(options: list):
    print("-" * 55)
    for command in commands:
        print(f"\n{command} " + " " * (7 - len(command)) + f"- {commands_help[command]}")
    print("\n" + "-" * 55)

commands = {
    "x"      : my_exit,
    "help"   : help,
    "add"    : add,
    "rm"     : remove,
    "clear"  : clear_,
    "search" : search,
    "ls"     : view_whole_file,
    "mat"    : matrix,
    "vec"    : vector,
    "cat"    : mat_concat
}

commands_help = {
    "x"      : "exits the application",
    "help"   : "displays this list of command descriptions",
    "add"    : "add a object to the file",
    "rm"     : "remove a object from the file",
    "clear"  : "remove all objects in a file",
    "search" : "search for a object name in a file",
    "ls"     : "view all objects in a file",
    "mat"    : "access the matrix calculator",
    "vec"    : "access the vector calculator",
    "cat"    : "concatenate linear transformations"
}
# End database functions


def start():
    while True:
        user_input = input("maininator> ").lower()
        
        user_input = user_input.split(" ")
        user_command = user_input[0]
        
        if "default" in user_input:
            print("Can't use file defaults")
            continue
        
        if user_command not in commands:
            print("Not a command use 'help' to see a list of all commands")
            continue
        commands[user_command](user_input[1:])

start()
