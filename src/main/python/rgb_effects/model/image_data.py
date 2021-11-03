from statistics import mean, stdev
from PIL import Image
import os
import math

class ImageData:
  def __init__(self, image):
    self.image = image

    self.r = list(self.image.getdata(band=0))
    self.g = list(self.image.getdata(band=1))
    self.b = list(self.image.getdata(band=2))

    self.isGray = self.r == self.g == self.b
    self.height = self.image.height
    self.width = self.image.width
    self.size = self.height * self.width

    self.setHistogramAndRange()
    self.setAccHistogram()
    self.setHistogramMean()
    self.setHistogramStDev()

  def setHistogramAndRange(self):
    self.rHistogram = [0] * 256
    self.gHistogram = [0] * 256
    self.bHistogram = [0] * 256

    self.rRange = [256, -1]
    self.gRange = [256, -1]
    self.bRange = [256, -1]

    for i in range(self.size):
      rTone = self.r[i]
      gTone = self.g[i]
      bTone = self.b[i]

      self.setMinMax(rTone, self.rRange)
      self.setMinMax(gTone, self.gRange)
      self.setMinMax(bTone, self.bRange)

      self.rHistogram[rTone] += 1 / self.size
      self.gHistogram[gTone] += 1 / self.size
      self.bHistogram[bTone] += 1 / self.size

  def setMinMax(self, x, minMax):
    if x < minMax[0]:
      minMax[0] = x
    if x > minMax[1]:
      minMax[1] = x

  def setAccHistogram(self):
    self.rAccHistogram = [0] * 256
    self.gAccHistogram = [0] * 256
    self.bAccHistogram = [0] * 256

    for i in range(256):
      self.rAccHistogram[i] = self.rAccHistogram[i - 1] + self.rHistogram[i]
      self.gAccHistogram[i] = self.gAccHistogram[i - 1] + self.gHistogram[i]
      self.bAccHistogram[i] = self.bAccHistogram[i - 1] + self.bHistogram[i]

  def setHistogramMean(self):
    self.rBrightness = self.gBrightness = self.bBrightness = 0

    for i in range(256):
      self.rBrightness += i * self.rHistogram[i]
      self.gBrightness += i * self.gHistogram[i]
      self.bBrightness += i * self.bHistogram[i]

  def setHistogramStDev(self):
    self.rContrast = self.gContrast = self.bContrast = 0

    for i in range(256):
      self.rContrast += self.rHistogram[i] * (i - self.rBrightness) ** 2
      self.gContrast += self.gHistogram[i] * (i - self.gBrightness) ** 2
      self.bContrast += self.bHistogram[i] * (i - self.bBrightness) ** 2

    self.rContrast = math.sqrt(self.rContrast)
    self.gContrast = math.sqrt(self.gContrast)
    self.bContrast = math.sqrt(self.bContrast)

  def setEntropy(self):
    for i in range(256):
      rP = self.rHistogram[i]
      gP = self.gHistogram[i]
      bP = self.bHistogram[i]

      self.rEntropy += rP * math.log(rP, 2)
      self.gEntropy += gP * math.log(gP, 2)
      self.bEntropy += bP * math.log(bP, 2)
    
    self.rEntropy *= -1
    self.gEntropy *= -1
    self.bEntropy *= -1
