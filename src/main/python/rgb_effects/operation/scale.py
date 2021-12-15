from PIL import Image
from copy import deepcopy
from math import floor

from rgb_effects.model import image_data as id
from rgb_effects.operation import geometric_transformation

def apply(input_data, param):
  x_scale_factor, y_scale_factor, interpolation_method, __ = param
  size_out_image = (input_data.width * x_scale_factor, input_data.height * y_scale_factor)
  coordinates_map = lambda i, j: (floor(i / x_scale_factor), floor(j / y_scale_factor))

  return geometric_transformation.apply(input_data, size_out_image, coordinates_map, interpolation_method)
