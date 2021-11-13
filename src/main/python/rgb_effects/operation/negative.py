from copy import deepcopy

from rgb_effects.model import image_data as id

LUT = [i for i in reversed(list(range(256)))]

def apply(image_a):
  out_image = deepcopy(image_a)

  for band in range(3):
    for pixel in range(len(out_image[band])):
      out_image[band][pixel] = LUT[image_a[band][pixel]]
  return id.dataToImage(out_image)
