from copy import deepcopy

from rgb_effects.model import image_data as id

def calculate_absolute_difference(_, param):
  image_a, image_b, __ = param
  diff_image = deepcopy(image_a)
  for pixel in range(len(diff_image)):
    for band in range(3):
      diff_image[band][pixel] = abs(image_a[band][pixel] - image_b[band][pixel])
  return id.dataToImage(diff_image)