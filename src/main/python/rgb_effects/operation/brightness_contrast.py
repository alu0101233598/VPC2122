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
  for i in range(256):
    current_value = int(round(a_slope[n] * i + b_offset[n]))
    if current_value > 255:
      current_value = 255
    LUT.append(current_value)

  # Apply transforamtion
  converted_image = image_data
  for pixel in range(len(converted_image)):
    for n, band in enumerate(converted_image):
      converted_image[n][pixel] = LUT[band[pixel]]
  return id.dataToImage(converted_image)