import print_stuff as ps
import numpy as np

def add(vec1: list, vec2: list) -> list:
    new_vec = []
    iterations = len(vec1)
    for idx in range(iterations):
        new_vec.append(vec1[idx] + vec2[idx])
    return new_vec

def sub(vec1: list, vec2: list) -> list:
    return add(vec1, scale(vec2, -1))

def scale(vec1: list, scale: float) -> list:
    new_vec = []
    iterations = len(vec1)
    for idx in range(iterations):
        new_vec.append(vec1[idx] * scale)
    return new_vec

def mag(vec: list) -> float:
    magnitude = 0
    iterations = len(vec)
    for idx in range(iterations):
        magnitude += vec[idx] * vec[idx]
    return np.sqrt(magnitude)

def dot(vec1: list, vec2: list) -> float:
    vec_mults = []
    iterations = len(vec1)
    for idx in range(iterations):
        vec_mults.append(vec1[idx] * vec2[idx])
    dot_return = 0
    dot_string = ""
    for idx in range(iterations):
        dot_return += vec_mults[idx]
        dot_string += f"{vec1[idx]} * {vec2[idx]} + " if idx != iterations - 1 else f"{vec1[idx]} * {vec2[idx]}"
    print()
    ps.prettify_vector(vec1)
    ps.prettify_vector(vec2)
    print(dot_string)
    return dot_return

def distance(vec1: list, vec2: list) -> float:
    pass

def normalize(vec: list) -> list:
    pass

def point(vec: list, vec_to_point: list) -> list:
    pass