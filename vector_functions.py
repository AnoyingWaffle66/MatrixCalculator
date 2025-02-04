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
    # dot_string = ""
    for idx in range(iterations):
        dot_return += vec_mults[idx]
        # dot_string += f"{vec1[idx]}*{vec2[idx]}" 
        # dot_string += " + " if idx != iterations - 1 else ""
    # print()
    # print("Vector 1")
    # ps.prettify_vector(vec1)
    # print("Vector 2")
    # ps.prettify_vector(vec2)
    # print(f"Equation: {dot_string}\n")
    return dot_return

def distance(vec1: list, vec2: list) -> float:
    return mag(sub(vec2, vec1))

def normalize(vec: list) -> list:
    magnitude = mag(vec)
    print(f"\nmagnitude = {magnitude}" + "\n")
    normalized_vec = []
    dividend = 1/magnitude
    for value in vec:
        normalized_vec.append(value * dividend)
    print("%.4f * %s = %s" % (magnitude, ps.prettify_vector(vec), ps.prettify_vector(normalized_vec))) 
    return normalized_vec

def point(vec_to_point: list, vec: list) -> list:
    magnitude = mag(vec_to_point) / mag(vec)
    return scale(vec, magnitude)

def proj(vec1: list, vec2: list) -> list:
    vec1_str = ps.prettify_vector(vec1)
    vec2_str = ps.prettify_vector(vec2)
    numerator = dot(vec1, vec2)
    print("\n%s\ndot\n%s\n= %.2f\n" % (vec1_str, vec2_str, numerator))
    denomenator = dot(vec2, vec2)
    print("%s\ndot\n%s\n= %.2f\n" % (vec2_str, vec2_str, denomenator))
    magnitude = numerator/denomenator
    print("scalar =\n%.2f / %.2f\n= %.2f\n" % (numerator, denomenator, magnitude))
    projection = scale(vec2, magnitude)
    projection_str = ps.prettify_vector(projection)
    print("v1 = scalar * w\n%.2f * %s\n= %s" % (magnitude, vec2_str, projection_str) + "\n")
    perpindicular_vec_str = ps.prettify_vector(sub(vec1, projection))
    print("v2 = v - v1\n%s - %s\n= %s\n" % (vec1_str, projection_str, perpindicular_vec_str))
    return projection