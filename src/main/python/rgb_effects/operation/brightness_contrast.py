from copy import deepcopy

from rgb_effects.model import image_data as id

def apply_transformation(image_data, user_values):
  # Calculate parameters
  a_slope = []
  b_offset = []
  for n, contrast in enumerate(image_data.contrastIter()):
    a_slope.append(user_values[1][n] / contrast)
  for n, brightness in enumerate(image_data.brightnessIter()):
    b_offset.append(user_values[0][n] - a_slope[n] * brightness)
  
  # Calculate LUT
  LUT = []
  for n in range(len(a_slope)):
    LUT.append([])
    for i in range(256):
      current_value = int(round(a_slope[n] * i + b_offset[n]))
      if current_value > 255:
        current_value = 255
      LUT[n].append(current_value)

  # Apply transformation
  converted_image = deepcopy(image_data)
  for pixel in range(len(converted_image)):
    for n, band in enumerate(converted_image):
      band[pixel] = LUT[n][band[pixel]]
  return id.dataToImage(converted_image)