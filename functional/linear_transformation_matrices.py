import math as m
import numpy as np

def to_rad(theta: float):
    return theta * m.pi / 180

def cos_and_sin(theta):
    theta = to_rad(theta)
    return np.cos(theta), np.sin(theta)

def rot2(theta: float) -> list:
    cos, sin = cos_and_sin(theta)
    return [
        cos, -sin,
        sin, cos
    ], 2

def rot3x(theta: float) -> list:
    cos, sin = cos_and_sin(theta)
    return [
        1, 0,      0,
        0, cos, -sin,
        0, sin, cos
    ], 3
    
def rot3y(theta: float) -> list:
    cos, sin = cos_and_sin(theta)
    return [
        cos,  0, sin,
        0,    1, 0,
        -sin, 0, cos
    ], 3

def rot3z(theta: float) -> list:
    cos, sin = cos_and_sin(theta)
    return [
        cos, -sin, 0,
        sin, cos,  0,
        0,   0,    1
    ], 3

def rot3all(values: list) -> list:
    theta = values[0]
    x = values[1]
    y = values[2]
    z = values[3]
    cos, sin = cos_and_sin(theta)
    return [
        m.pow(x, 2) * (1 - cos) + cos, x * y * (1 - cos) - z * sin, x * z * (1 - cos) + y * sin,
        x * y * (1 - cos) + z * sin, m.pow(y, 2) * (1 - cos) + cos, y * z * (1 - cos) - x * sin,
        x * z * (1 - cos) - y * sin, y * z * (1 - cos) + x * sin, m.pow(z, 2) * (1 - cos) + cos
    ], 3

def scale2d(values: list) -> list:
    x = values[0]
    y = values[1]
    return [
        x, 0,
        0, y
    ], 2

def scale3d(values: list) -> list:
    x = values[0]
    y = values[1]
    z = values[2]
    return [
        x, 0, 0,
        0, y, 0,
        0, 0, z
    ], 3

def ortho2x(values: list=None) -> list:
    return [
        1, 0,
        0, 0
    ], 2

def ortho2y(values: list=None) -> list:
    return [
        0, 0,
        0, 1
    ], 2

def ortho3z(values: list=None) -> list:
    return [
        1, 0, 0,
        0, 1, 0,
        0, 0, 0
    ], 3

def ortho3y(values: list=None) -> list:
    return [
        1, 0, 0,
        0, 0, 0,
        0, 0, 1
    ], 3

def ortho3x(values: list=None) -> list:
    return [
        0, 0, 0,
        0, 1, 0,
        0, 0, 1
    ], 3

def aboutx(values: list=None) -> list:
    return [
        1, 0,
        0, -1
    ], 2

def abouty(values: list=None) -> list:
    return [
        -1, 0,
        0, 1
    ], 2

def one_minus_two_pow(base: float) -> float:
    return 1 - 2 * m.pow(base, 2)

def about2d(values: list) -> list:
    x = values[0]
    y = values[1]
    xy = -2 * x * y
    return [
        one_minus_two_pow(x), xy,
        xy, one_minus_two_pow(y)
    ], 2

def about3d(values: list) -> list:
    x = values[0]
    y = values[1]
    z = values[2]
    xy = -2 * x * y
    xz = -2 * x * z
    yz = -2 * y * z
    return [
        one_minus_two_pow(x), xy, xz,
        xy, one_minus_two_pow(y), yz,
        xz, yz, one_minus_two_pow(z)
    ], 3

def horizontal_skew(skew_value: float) -> list:
    return [
        1, skew_value,
        0, 1
    ], 2

def vertical_skew(skew_value: float) -> float:
    return [
        1, 0,
        skew_value, 1
    ], 2

def z_skew(values: list) -> list:
    x = values[0]
    y = values[1]
    return [
        1, 0, x,
        0, 1, y,
        0, 0, 1
    ], 3

def y_skew(values: list) -> list:
    x = values[0]
    z = values[1]
    return [
        1, x, 0,
        0, 1, 0,
        0, z, 1
    ], 3

def x_skew(values: list) -> list:
    y = values[0]
    z = values[1]
    return [
        1, 0, 0,
        y, 1, 0,
        z, 0, 1
    ], 3