from PyQt5.QtWidgets import QMdiSubWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from PIL.ImageQt import ImageQt

from rgb_effects.model.image_data import ImageData

class ImageDisplay(QMdiSubWindow):
  def __init__(self, image, title):
    super().__init__()
    self.title = title
    self.setWindowTitle(self.title)
    qimage = ImageQt(image)
    pixmap = QPixmap.fromImage(qimage)
    label = QLabel(self, alignment=Qt.AlignCenter)
    label.setMouseTracking(True)
    label.setPixmap(pixmap)
    self.setWidget(label)
    self.image = ImageData(image)
