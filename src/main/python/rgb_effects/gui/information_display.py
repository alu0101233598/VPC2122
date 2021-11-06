
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from rgb_effects.gui.image_label import ImageLabel

import io
from PIL import Image

class InformationDisplay(QDialog):
  def __init__(self, imageSubWin, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.image = imageSubWin.image
    self.data = imageSubWin.image_data
    self.title = imageSubWin.title

    self.format = str(self.image.format)
    self.size = str(self.image.size)
    self.isGray = self.data.isGray
    self.rgbOrGrayscale = "Grayscale" if self.isGray else "RGB"

    self.range = list(map(str, [self.data.rRange, self.data.gRange, self.data.bRange]))
    self.brightness = list(map(self.roundedStr, [self.data.rBrightness, self.data.gBrightness, self.data.bBrightness]))
    self.contrast = list(map(self.roundedStr, [self.data.rContrast, self.data.gContrast, self.data.bContrast]))
    self.entropy = list(map(self.roundedStr, [self.data.rEntropy, self.data.gEntropy, self.data.bEntropy]))

    self.dataStr = ""
    properties = [("Range", self.range), ("Brightness", self.brightness), ("Contrast", self.contrast), ("Entropy", self.entropy)]
    colors = ["Grayscale"] if self.isGray else ["Red", "Green", "Blue"]
    for i in range(len(properties)):
      for j in range(len(colors)):
        self.dataStr += colors[j] + " " + properties[i][0] + ": " + properties[i][1][j] + "\n"
      self.dataStr += "\n"

    self.layout = QVBoxLayout()
    self.label = QLabel()
    self.label.setText("\nFile Type: " + self.format + "\n" + \
                       "Size: " + self.size + "\n" + \
                       "RGB or Grayscale: " + self.rgbOrGrayscale + "\n\n" + \
                       self.dataStr)

    self.layout.addWidget(ImageLabel(self.image, self, alignment=Qt.AlignCenter))
    self.layout.addWidget(self.label)
    self.layout.setAlignment(Qt.AlignCenter)
    self.setLayout(self.layout)

    self.setWindowTitle(self.title + " Information")
    self.setFixedSize(400 + self.image.size[0] * 1.2, (500 if self.isGray else 800) + self.image.size[1] * 1.2)
    self.show()

  def roundedStr(self, x):
    return str(round(x, 2))
