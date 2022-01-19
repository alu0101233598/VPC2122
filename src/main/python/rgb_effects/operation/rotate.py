from PIL import Image
from copy import deepcopy
from math import sin, cos, sqrt, radians, floor

from rgb_effects.model import image_data as id
from rgb_effects.operation import geometric_transformation

def rotate_90(image_data):
  transposed_data = deepcopy(image_data)
  transposed_data.width = image_data.height
  transposed_data.height = image_data.width
  
  for n, _ in enumerate(transposed_data):
    for i in range(transposed_data.height):
      for j in range(transposed_data.width):
        transposed_data[n][i * transposed_data.width + j] = image_data[n][(image_data.height - j - 1) * image_data.width + i]

  return id.dataToImage(transposed_data)

def rotate_270(image_data):
  transposed_data = deepcopy(image_data)
  transposed_data.width = image_data.height
  transposed_data.height = image_data.width
  
  for n, _ in enumerate(transposed_data):
    for i in range(transposed_data.height):
      for j in range(transposed_data.width):
        transposed_data[n][i * transposed_data.width + j] = image_data[n][(j + 1) * image_data.width - i - 1]

  return id.dataToImage(transposed_data)

def rotate_180(image_data):
  transposed_data = deepcopy(image_data)
  
  for n, _ in enumerate(transposed_data):
    for i in range(transposed_data.height):
      for j in range(transposed_data.width):
        transposed_data[n][i * transposed_data.width + j] = image_data[n][(image_data.height - i) * image_data.width - j - 1]

  return id.dataToImage(transposed_data)

def rotate_and_draw(input_data, param):
  angle, __ = param
  rad = radians(angle)
  coordinates_map_dt = lambda i, j: (i * cos(rad) - j * sin(rad), i * sin(rad) + j * cos(rad))

  a = (0, 0)
  b = coordinates_map_dt(input_data.width, 0)
  c = coordinates_map_dt(0, input_data.height)
  d = coordinates_map_dt(input_data.width, input_data.height)
  
  origin = (min(a[0], b[0], c[0], d[0]), min(a[1], b[1], c[1], d[1]))
  end = (max(a[0], b[0], c[0], d[0]), max(a[1], b[1], c[1], d[1]))
  size_out_image = (round(end[0] - origin[0]), round(end[1] - origin[1]))

  output_data = deepcopy(input_data)
  output_data.width = size_out_image[0]
  output_data.height = size_out_image[1]
  output_data.size = output_data.width * output_data.height
  output_data.r = [0] * output_data.size
  output_data.g = [0] * output_data.size
  output_data.b = [0] * output_data.size
  counter_set = set([])

  for i in range(0, input_data.height):
    for j in range(0, input_data.width):
      pixel_it = i * input_data.width + j
      x, y = coordinates_map_dt(j, i)
      x = floor(x - origin[0])
      y = floor(y - origin[1])
      if x < 0 or y < 0 or x >= output_data.width or y >= output_data.height:
        continue
      counter_set.add((x, y))
      for n, _ in enumerate(input_data):
        output_data[n][y * output_data.width + x] = input_data[n][pixel_it] 
  return id.dataToImage(output_data), output_data.size - len(counter_set)

def apply(input_data, param):
  angle, interpolation_method, __ = param

  rad = radians(angle)
  coordinates_map_dt = lambda i, j: (i * cos(rad) - j * sin(rad), i * sin(rad) + j * cos(rad))
  coordinates_map_it = lambda i, j: (i * cos(- rad) - j * sin(- rad), i * sin(- rad) + j * cos(- rad))
  
  a = (0, 0)
  b = coordinates_map_dt(input_data.width, 0)
  c = coordinates_map_dt(0, input_data.height)
  d = coordinates_map_dt(input_data.width, input_data.height)

  origin = (min(a[0], b[0], c[0], d[0]), min(a[1], b[1], c[1], d[1]))
  end = (max(a[0], b[0], c[0], d[0]), max(a[1], b[1], c[1], d[1]))
  size_out_image = (round(end[0] - origin[0]), round(end[1] - origin[1]))  
  return geometric_transformation.apply(input_data, size_out_image, coordinates_map_it, interpolation_method, origin)
