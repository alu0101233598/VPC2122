from PIL import Image
from copy import deepcopy
from math import floor

from rgb_effects.model import image_data as id

interpolation_methods = {
  "Bilinear": lambda p, q, a, b, c, d:
    (d if q > 0.5 else b) if p > 0.5 else (c if q > 0.5 else a)
  ,
  "Nearest Neighbour": lambda p, q, a, b, c, d:
    c + (d - c) * p + (a - c) * q + (b + c - a - d) * p * q
}

def apply(input_data, size_out_image, coordinates_map, interpolation_method):
  output_data = deepcopy(input_data)
  output_data.width = size_out_image[0]
  output_data.height = size_out_image[1]
  output_data.size = output_data.width * output_data.height
  output_data.r = [0] * output_data.size
  output_data.g = [0] * output_data.size
  output_data.b = [0] * output_data.size

  for i in range(1, output_data.height - 2):
    for j in range(1, output_data.width - 2):
      pixel_it = i * output_data.width + j
      x, y = coordinates_map(j, i)
      p = x - floor(x)
      q = y - floor(y)
      for n, _ in enumerate(output_data):
        a = input_data[n][floor(y) * input_data.width + floor(x)]
        b = input_data[n][(floor(y) + 1) * input_data.width + floor(x)]
        c = input_data[n][floor(y) * input_data.width + (floor(x) + 1)]
        d = input_data[n][(floor(y) + 1) * input_data.width + (floor(x) + 1)]
        
        output_data[n][pixel_it] = interpolation_methods[interpolation_method](p, q, a, b, c, d)

  return id.dataToImage(output_data)
