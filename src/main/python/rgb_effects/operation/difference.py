from copy import deepcopy

from rgb_effects.model import image_data as id

LUT = []

def initialize_lut():
  for i in range(256):
    LUT.append({})
    for j in range(i, 256):
      LUT[i][j] = abs(j - i)

def calculate_absolute_difference(_, param):
  image_a, image_b, __ = param
  diff_image = deepcopy(image_a)

  if not len(LUT):
    initialize_lut()

  for pixel in range(len(diff_image)):
    for band in range(3):
      pixel_a = image_a[band][pixel]
      pixel_b = image_b[band][pixel]
      value = LUT[pixel_a][pixel_b] if pixel_a < pixel_b else LUT[pixel_b][pixel_a]
      diff_image[band][pixel] = value
      
  diff_image.isGray = False
  return id.dataToImage(diff_image)

def calculate_changes(_, param):
  image_a, image_b, threshold, __ = param
  change_image = deepcopy(image_a)

  if not len(LUT):
    initialize_lut()

  for pixel in range(len(change_image)):
    current_change = [0, 0, 0]
    for n, band in enumerate(change_image):
      pixel_a = image_a[n][pixel]
      pixel_b = image_b[n][pixel]
      value = LUT[pixel_a][pixel_b] if pixel_a < pixel_b else LUT[pixel_b][pixel_a]
      if value > threshold:
        current_change[n] = 255
    if current_change != [0, 0, 0]:
      for n in range(3):
        change_image[n][pixel] = current_change[n]
  change_image.isGray = False
  return id.dataToImage(change_image)