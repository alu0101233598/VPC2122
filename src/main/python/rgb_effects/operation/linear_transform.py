from copy import deepcopy

from rgb_effects.model import image_data as id

def apply(image_a, param):
  points, __ = param
  out_image = deepcopy(image_a)

  if points[0][0] != 0:
    if points[0][0] != 1:
      points.insert(0, [points[0][0] - 1, points[0][0] - 1])
    points.insert(0, [0, 0])
  if points[-1][0] != 255:
    if points[-1][0] != 254:
      points.append([points[-1][0] + 1, points[-1][0] + 1])
    points.append([255, 255])

  LUT = []
  for i in range(len(points) - 1):
    xi = points[i][0]
    xf = points[i + 1][0]

    yi = points[i][1]
    yf = points[i + 1][1]

    m = (yf - yi) / (xf - xi)
    n = yi - m * xi

    for x in range(xi, xf + 1):
      y = round(m * x + n)
      LUT.append(y)

  for n, band in enumerate(out_image):
    for pixel in range(len(out_image)):
      band[pixel] = LUT[image_a[n][pixel]]
  return id.dataToImage(out_image)
