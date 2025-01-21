def MCA(mult: int, const: int, add: int) -> int:
    return mult * const + add

def multiply(mat1: list, mat2: list, inner: int, outer_left: int, outer_right: int) -> list:
    mat_arr = []
    for mat_count in range(inner):
        temp_matrix = []
        for left in range(outer_left):
            for right in range(outer_right):
                temp_matrix.append(mat1[MCA(left, inner, mat_count)] * mat2[MCA(mat_count, outer_right, right)])
        mat_arr.append(temp_matrix)
    for add_arr_idx in range(1, len(mat_arr)):
        mat_arr[0] = add(mat_arr[0], mat_arr[add_arr_idx])
    return mat_arr[0]

def add(mat1: list, mat2: list) -> list:
    values = []
    for mat_idx in range(len(mat1)):
        values.append(mat1[mat_idx] + mat2[mat_idx])
    return values

def subtract(mat1: list, mat2: list) -> list:
    return add(mat1, scale(mat2, -1))

def scale(mat: list, scale: float) -> list:
    values = []
    for mat_idx in range(len(mat)):
        values.append(mat[mat_idx] * scale)

def determinate(mat: list, side: int) -> float:
    if(side == 1):
        return mat[0]
    value = 0
    for column in range(0, side):
        matrix_to_det = []
        for row in range(1, side):
            for extra in range(0, side):
                determin_append = MCA(row, side, extra)
                if determin_append != MCA(row, side, column):
                    matrix_to_det.append(mat[determin_append])
        value += pow(-1, column) * mat[column] * determinate(matrix_to_det, side - 1)
    return value

def transpose(mat: list, left: int, right: int) -> list:
    list_to_return = []
    for column in range(right):
        for row in range(left):
            list_to_return.append(mat[MCA(row, right, column)])
    return list_to_return

def inverse(mat: list, side: int):
    mat_to_return = []
    for matrix_pos in range(0, len(mat)):
        mat_to_return.append(0)
        mat_to_det = []
        exponent_list = []
        for a in range(0, side):
            for b in range(0, side):
                idx = MCA(a, side, b)
                idx_mod = idx % side
                idx_div = int(idx / side)
                if idx_mod != matrix_pos % side and idx_div != int(matrix_pos / side):
                    mat_to_det.append(mat[idx])
                exponent_list.append(a+b)
        cofactor = pow(-1, exponent_list[matrix_pos]) * MCA(mat_to_det, side - 1)
        mat_to_return[matrix_pos] = cofactor
    mat_to_return = transpose(mat_to_return, side, side)
    inverse_determinate = 1/determinate
    mat_to_return = scale(mat_to_return, inverse_determinate)
    pass

def solve(mat1: dict, mat2: dict):
    pass
