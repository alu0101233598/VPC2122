from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal

class ImageLabel(QLabel):
  mouse_moved = pyqtSignal(tuple)

  def __init__(self, image, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.image =  image
    data = self.image.convert("RGB").tobytes("raw", "RGB")
    qimage = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
    self.setMouseTracking(True)
    self.setPixmap(pixmap)
    
  def mouseMoveEvent(self, event):
    rgb = self.image.getpixel((event.x(), event.y()))
    self.mouse_moved.emit((event.x(), event.y(), *rgb))