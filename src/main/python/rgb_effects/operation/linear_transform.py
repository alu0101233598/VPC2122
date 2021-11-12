from copy import deepcopy

from rgb_effects.model import image_data as id

def apply(_, param):
  image_a, points, __ = param
  out_image = deepcopy(image_a)

  i = 0
  LUT = []
  for x in range(256):
    y = x
    if x > points[i + 1][0] and i < len(points) - 2:
      i += 1
    
    xi = points[i][0]
    xf = points[i + 1][0]

    if xi != xf:
      yi = points[i][1]
      yf = points[i + 1][1]

      m = (yf - yi) // (xf - xi)
      n = yi - m * xi

      y = m * x + n
    else:
      print("Warning: Match on the pixel " + str(xi) + \
            ". It has been assigned the same level as the input image")
    LUT.append(y)

  for band in range(3):
    for pixel in range(len(out_image[band])):
      out_image[band][pixel] = LUT[image_a[band][pixel]]
  return id.dataToImage(out_image)
