from copy import deepcopy

from rgb_effects.model import image_data as id

def apply(image_a, param):
  gamma, __ = param
  out_image = deepcopy(image_a)

  LUT = []
  for band in range(1 if image_a.isGray else 3):
    LUT.append([])
    for i in range(256):
      LUT[band].append(255 * pow(i / 255, gamma[band]))

  for band in range(3):
    for pixel in range(len(out_image[band])):
      out_image[band][pixel] = LUT[0 if image_a.isGray else band][image_a[band][pixel]]
  return id.dataToImage(out_image)
