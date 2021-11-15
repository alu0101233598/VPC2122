from copy import deepcopy

from rgb_effects.model import image_data as id

def apply(image_a, param):
  gamma, __ = param
  out_image = deepcopy(image_a)

  LUT = []
  for n in range(len(gamma)):
    LUT.append([])
    for i in range(256):
      LUT[n].append(round(255 * pow(i / 255, gamma[n])))

  for n in range(len(gamma)):
    for pixel in range(len(out_image)):
      out_image[n][pixel] = LUT[n][image_a[n][pixel]]
  return id.dataToImage(out_image)
