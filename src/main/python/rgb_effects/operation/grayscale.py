from PIL import Image
from math import floor
from copy import deepcopy

from rgb_effects.model import image_data as id

grayscaleLUT = [
  [r * 0.299 for r in range(256)],
  [g * 0.587 for g in range(256)],
  [b * 0.114 for b in range(256)],
]

def NTSC_conversion(image_data):
  grayscale_data = deepcopy(image_data)
  if image_data.isGray:
    return grayscale_data.image
  for pixel in range(len(grayscale_data)):
    grayscale_value = 0
    for n, band in enumerate(grayscale_data):
      grayscale_value += grayscaleLUT[n][band[pixel]]
    grayscale_data.r[pixel] = grayscale_data.g[pixel] = grayscale_data.b[pixel] = floor(grayscale_value)
  return id.dataToImage(grayscale_data)
