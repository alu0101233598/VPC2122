from copy import deepcopy

from rgb_effects.model import image_data as id

def apply(_, param):
  image_a, image_b, __ = param
  out_image = deepcopy(image_a)

  cum_histogram_image_a = [image_a.rCumHistogram] if image_a.isGray else [image_a.rCumHistogram, image_a.gCumHistogram, image_a.bCumHistogram]
  cum_histogram_image_b = [image_b.rCumHistogram] if image_b.isGray else [image_b.rCumHistogram, image_b.gCumHistogram, image_b.bCumHistogram]

  LUT = []
  for i in range(3):
    LUT.append([])
    for j in range(256):
      LUT[i].append(search(cum_histogram_image_a[0 if image_a.isGray else i][j], cum_histogram_image_b[0 if image_b.isGray else i]))

  for band in range(3):
    for pixel in range(len(out_image)):
      out_image[band][pixel] = LUT[band][image_a[band][pixel]]
  out_image.isGray = False
  return id.dataToImage(out_image)

def search(x, arr):
  pre = arr[0]
  for i, elem in enumerate(arr):
    if x <= elem:
      return i - 1 if abs(x - pre) < abs(x - elem) else i
    pre = elem
  return arr[-1]
