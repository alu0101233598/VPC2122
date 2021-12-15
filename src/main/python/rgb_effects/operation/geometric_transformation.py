from PIL import Image
from copy import deepcopy
from math import floor

from rgb_effects.model import image_data as id

interpolation_methods = {
  "Bilinear": lambda p, q, a, b, c, d: {
    (b if q > 0.5 else d) if p > 0.5 else (a if q > 0.5 else c)
  },
  "Nearest Neighbour": lambda p, q, a, b, c, d: {
    c + (d - c) * p + (a - c) * q + (b + c - a - d) * p * q
  }
}

def apply(input_data, size_out_image, coordinates_map, interpolation_method):
  output_data = deepcopy(input_data)
  output_data.width = size_out_image[0]
  output_data.height = size_out_image[1]

  for i in range(output_data.height):
    for j in range(output_data.width):
      pixel_it = i * input_data.width + j
      x, y = coordinates_map(i, j)
      for n, _ in enumerate(output_data):
        # p = x - floor(x)
        # q = y - floor(y)
        print(len(input_data[n]), (floor(y) + 1) * input_data.width + floor(x))
        # a = input_data[n][(floor(y) + 1) * input_data.width + floor(x)]
        # b = input_data[n][(floor(y) + 1) * input_data.width + (floor(x) + 1)]
        # c = input_data[n][floor(y) * input_data.width + floor(x)]
        # d = input_data[n][floor(y) * input_data.width + (floor(x) + 1)]
        
        # output_data[n][pixel_it] = interpolation_methods[interpolation_method](p, q, a, b, c, d)

  return id.dataToImage(output_data)
