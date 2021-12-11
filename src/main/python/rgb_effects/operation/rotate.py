from PIL import Image
from copy import deepcopy

from rgb_effects.model import image_data as id

def rotate_90(image_data):
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

def rotate_270(image_data):
  transposed_data = deepcopy(image_data)
  transposed_data.width = image_data.height
  transposed_data.height = image_data.width
  
  for n, _ in enumerate(transposed_data):
    for i in range(transposed_data.height):
      for j in range(transposed_data.width):
        transposed_data[n][i * transposed_data.width + j] = image_data[n][(image_data.height - j - 1) * image_data.width + i]

  return id.dataToImage(transposed_data)
