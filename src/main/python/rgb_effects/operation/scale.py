from PIL import Image
from copy import deepcopy
from math import floor

from rgb_effects.model import image_data as id
from rgb_effects.operation import geometric_transformation

def apply(input_data, param):
  x_scale_factor, y_scale_factor, interpolation_method, __ = param
  coordinates_map_dt = lambda i, j: (i * x_scale_factor, j * y_scale_factor)
  coordinates_map_it = lambda i, j: (i / x_scale_factor, j / y_scale_factor)

  size_out_image = tuple(map(lambda x: floor(x), coordinates_map_dt(input_data.width, input_data.height)))
  return geometric_transformation.apply(input_data, size_out_image, coordinates_map_it, interpolation_method)
