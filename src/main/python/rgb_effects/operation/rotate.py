from PIL import Image
from copy import deepcopy
from math import sin, cos, sqrt, radians

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

def apply(input_data, param):
  angle, interpolation_method, __ = param

  rad = radians(angle)
  coordinates_map_dt = lambda i, j: (i * cos(rad) - j * sin(rad), i * sin(rad) + j * cos(rad))
  coordinates_map_it = lambda i, j: (i * cos(- rad) - j * sin(- rad), i * sin(- rad) + j * cos(- rad))
  
  b = coordinates_map_dt(input_data.width, 0)
  c = coordinates_map_dt(0, input_data.height)
  d = coordinates_map_dt(input_data.width, input_data.height)

  if 0 <= angle < 90 or - 360 <= angle < -270:
    size_out_image = (b[0] - c[0], d[1])
  if 90 <= angle < 180 or - 270 <= angle < -180:
    size_out_image = (- d[0], b[1] - c[1])
  if 180 <= angle < 270 or - 180 <= angle < -90:
    size_out_image = (c[0] - b[0], - d[1])
  if 270 <= angle <= 360 or - 90 <= angle < 0:
    size_out_image = (d[0], c[1] - b[1])
  
  size_out_image = (round(size_out_image[0]), round(size_out_image[1]))

  return geometric_transformation.apply(input_data, size_out_image, coordinates_map_it, interpolation_method)
