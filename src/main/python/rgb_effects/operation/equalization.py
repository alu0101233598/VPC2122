from copy import deepcopy

from rgb_effects.model import image_data as id

def apply(image_a):
  out_image = deepcopy(image_a)

  cum_histogram_image_a = [image_a.rCumHistogram] if image_a.isGray else [image_a.rCumHistogram, image_a.gCumHistogram, image_a.bCumHistogram]

  LUT = []
  for i in range(len(cum_histogram_image_a)):
    LUT.append([])
    for j in range(256):
      LUT[i].append(max(0, round(256 * cum_histogram_image_a[i][j]) - 1))

  for n, band in enumerate(out_image):
    for pixel in range(len(out_image)):
      band[pixel] = LUT[n][image_a[n][pixel]]
  return id.dataToImage(out_image)
