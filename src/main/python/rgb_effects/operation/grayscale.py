from PIL import Image
from math import floor

grayscaleLUT = [
  [r * 0.222 for r in range(256)],
  [g * 0.707 for g in range(256)],
  [b * 0.071 for b in range(256)],
]

def grayscale_conversion(image_data):
  grayscale_data = image_data
  if image_data.isGray:
    return grayscale_data.image
  for pixel in range(len(grayscale_data)):
    grayscale_value = 0
    for n, band in enumerate(grayscale_data):
      grayscale_value += grayscaleLUT[n][band[pixel]]
    grayscale_data.r[pixel] = grayscale_data.g[pixel] = grayscale_data.b[pixel] = floor(grayscale_value)
  
  images = []
  for band in grayscale_data:
    image = Image.new("L", (grayscale_data.width, grayscale_data.height))
    image.putdata(band)
    images.append(image)
  return Image.merge("RGB", images)