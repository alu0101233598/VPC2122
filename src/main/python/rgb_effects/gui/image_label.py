from PyQt5.QtWidgets import QLabel, QWidget, QRubberBand
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QRect, QSize
from PIL import Image

from rgb_effects.common.image_signals import ImageSignals
class ImageLabel(QLabel):
  def __init__(self, image, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.signals = ImageSignals()
    self.image =  image
    self.rubberBand = None
    data = image.tobytes("raw", "RGB")
    qimage = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
    self.setMouseTracking(True)
    self.setPixmap(pixmap)

  def mousePressEvent(self, event):
    self.origin = event.pos()
    self.end = None
    if not self.rubberBand:
      self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
    self.rubberBand.setGeometry(QRect(self.origin, QSize()))
    self.rubberBand.show()
    
  def mouseMoveEvent(self, event):
    if event.x() < self.image.width and event.y() < self.image.height:
      if self.rubberBand:
        self.end = event.pos()
        self.rubberBand.setGeometry(QRect(self.origin, self.end).normalized())
      rgb = self.image.getpixel((event.x(), event.y()))
      self.signals.mouse_moved.emit((event.x(), event.y(), *rgb))

  def mouseReleaseEvent(self, event):
    self.rubberBand.hide()
    if self.end:
      crop = self.image.crop(box=(self.origin.x(), self.origin.y(), self.end.x(), self.end.y()))
      self.signals.selection_done.emit(crop)