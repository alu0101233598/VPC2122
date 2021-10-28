from statistics import mean, stdev
from PIL import Image
import os

class ImageData:
  def __init__(self, path):
    self.path = path
    self.directory, self.fileName = os.path.split(self.path)
    self.image = Image.open(path, 'r')
    self.data = self.image.getdata()

    self.r = []
    self.g = []
    self.b = []
    for sets in self.data:
      self.r.append(sets[0])
      self.g.append(sets[1])
      self.b.append(sets[2])

    self.isBw = self.r == self.g == self.b
    self.height = self.image.height
    self.width = self.image.width

    self.rRange = self.computeRange(self.r)
    self.gRange = self.computeRange(self.g)
    self.bRange = self.computeRange(self.b)

    self.rBrightness = mean(self.r)
    self.gBrightness = mean(self.g)
    self.bBrightness = mean(self.b)
    self.totalBrightness = mean([self.rBrightness,
                                 self.gBrightness,
                                 self.bBrightness])

    self.rContrast = stdev(self.r)
    self.gContrast = stdev(self.g)
    self.bContrast = stdev(self.b)
    self.totalContrast = mean([self.rContrast,
                               self.gContrast,
                               self.bContrast])

  def computeRange(self, array):
    return (min(array), max(array))