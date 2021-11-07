from copy import deepcopy

from rgb_effects.model import image_data as id

def calculate_difference(_, param):
  image_a, image_b = param
  return deepcopy(image_a.image)