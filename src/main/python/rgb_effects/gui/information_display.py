
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
    self.RgbOrGrayscale = "Grayscale" if self.data.isGray else "RGB"

    self.rRange = str(self.data.rRange)
    self.gRange = str(self.data.gRange)
    self.bRange = str(self.data.bRange)

    self.rBrightness = self.roundedStr(self.data.rBrightness)
    self.gBrightness = self.roundedStr(self.data.gBrightness)
    self.bBrightness = self.roundedStr(self.data.bBrightness)

    self.rContrast = self.roundedStr(self.data.rContrast)
    self.gContrast = self.roundedStr(self.data.gContrast)
    self.bContrast = self.roundedStr(self.data.bContrast)

    '''
    self.rEntropy = self.roundedStr(self.data.rEntropy)
    self.gEntropy = self.roundedStr(self.data.gEntropy)
    self.bEntropy = self.roundedStr(self.data.bEntropy)
    '''

    self.layout = QVBoxLayout()
    self.label = QLabel()
    self.label.setText("File Type: " + self.format + "\n" + \
                        "Size: " + self.size + "\n" + \
                        "RGB or Grayscale: " + self.RgbOrGrayscale + "\n\n" + \
                        "Red Range: " + self.rRange + "\n" + \
                        "Green Range: " + self.gRange + "\n" + \
                        "Blue Range: " + self.bRange + "\n\n" + \
                        "Red Brightness: " + self.rBrightness + "\n" + \
                        "Green Brightness: " + self.gBrightness + "\n" + \
                        "Blue Brightness: " + self.bBrightness + "\n\n" + \
                        "Red Contrast: " + self.rContrast + "\n" + \
                        "Green Contrast: " + self.gContrast + "\n" + \
                        "Blue Contrast: " + self.bContrast + "\n\n")# + \
                        #"Red Entropy: " + self.rEntropy + "\n")

    self.layout.addWidget(ImageLabel(self.image, self, alignment=Qt.AlignCenter))
    self.layout.addWidget(self.label)
    self.layout.setAlignment(Qt.AlignCenter)
    self.setLayout(self.layout)

    self.setWindowTitle(self.title + " Information")
    self.setFixedSize(350 + self.image.size[0] * 1.2, 600 + self.image.size[1] * 1.2)
    self.show()

  def roundedStr(self, x):
    return str(round(x, 2))
