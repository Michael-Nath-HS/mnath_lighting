import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    ambient_intensity = calculate_ambient(ambient, areflect)
    diffuse_intensity = calculate_diffuse(light, dreflect, normal)
    specular_intensity = calculate_specular(light, sreflect, view, normal)
    array_length = 3
    return limit_color([(int(ambient_intensity[i]) + int(diffuse_intensity[i]) + int(specular_intensity[i])) for i in range(array_length)])

def calculate_ambient(alight, areflect):
    if type(alight) != list and type(areflect) != list:
        return alight * areflect
    array_length = 3
    return [alight[i] * areflect[i] for i in range(array_length)]

def calculate_diffuse(light, dreflect, normal):
    normalize(normal)
    light_vector = light[0]
    light_color = light[1]
    normalize(light_vector)
    dot_prod = dot_product(normal, light_vector)
    array_length = 3
    return [light_color[i] * dreflect[i] * dot_prod for i in range(array_length)]

def calculate_specular(light, sreflect, view, normal):
    normalize(normal)
    light_vector = light[0]
    light_color = light[1]
    normalize(light_vector)
    scaled_magnitude = dot_product(normal, light_vector)
    array_length = 3
    t_vector = [normal[i] * scaled_magnitude for i in range(array_length)]
    s_vector = [t_vector[i] - light_vector[i] for i in range(array_length)]
    r_vector = [t_vector[i] + s_vector[i] for i in range(array_length)]   
    raised_exponent = 3
    scaled_dot_prod = dot_product(r_vector, view) ** (raised_exponent)
    return [light_color[i] * sreflect[i] * scaled_dot_prod for i in range(array_length)]

def limit_color(color):
    return [max(min(int(color[i]), 255), 0) for i in range(len(color))]

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
