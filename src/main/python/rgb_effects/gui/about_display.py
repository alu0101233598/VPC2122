
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from rgb_effects.gui.image_label import ImageLabel

import io

class AboutDisplay(QDialog):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.dataStr = "HOLA"

    self.layout = QVBoxLayout()
    self.label = QLabel()
    self.label.setText('Click <a href="https://github.com/alu0101233598/VPC2122">here</a> to see more')
    self.label.setOpenExternalLinks(True)

    self.layout.addWidget(self.label)
    self.layout.setAlignment(Qt.AlignCenter)
    self.setLayout(self.layout)

    self.setWindowTitle("About")
    self.show()
