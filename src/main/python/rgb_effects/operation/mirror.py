from PIL import Image
from copy import deepcopy

from rgb_effects.model import image_data as id

def horizontal_mirror(image_data):
  horizontal_mirror_data = deepcopy(image_data)
  
  for n, _ in enumerate(horizontal_mirror_data):
    for i in range(horizontal_mirror_data.height):
      for j in range(horizontal_mirror_data.width):
        horizontal_mirror_data[n][i * image_data.width + j] = image_data[n][(i + 1) * image_data.width - (j + 1)]

  return id.dataToImage(horizontal_mirror_data)

def vertical_mirror(image_data):
  vertical_mirror_data = deepcopy(image_data)
  
  for n, _ in enumerate(vertical_mirror_data):
    for i in range(vertical_mirror_data.height):
      for j in range(vertical_mirror_data.width):
        vertical_mirror_data[n][i * image_data.width + j] = image_data[n][(image_data.size - 1) - (i + 1) * image_data.width + j + 1]

  return id.dataToImage(vertical_mirror_data)
