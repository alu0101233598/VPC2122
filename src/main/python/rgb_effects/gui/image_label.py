from PyQt5.QtWidgets import QLabel, QWidget, QRubberBand
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QRect, QSize, Qt
from PIL import Image

from rgb_effects.common.image_signals import ImageSignals
class ImageLabel(QLabel):
  def __init__(self, image, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.signals = ImageSignals()
    self.image = image
    self.rubberBand = None
    data = image.tobytes("raw", "RGBA")
    self.qimage = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGBA8888)
    self.pixmap = QPixmap.fromImage(self.qimage)
    self.setFixedSize(self.image.width, self.image.height)
    self.setAlignment(Qt.AlignCenter)
    self.setMouseTracking(True)
    self.setPixmap(self.pixmap)

  def mousePressEvent(self, event):
    self.origin = event.pos()
    self.end = None
    if not self.rubberBand:
      self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
    self.rubberBand.setGeometry(QRect(self.origin, QSize()))
    self.rubberBand.show()
    
  def mouseMoveEvent(self, event):
    if self.qimage.valid(event.pos()):
      if self.rubberBand:
        self.end = event.pos()
        self.rubberBand.setGeometry(QRect(self.origin, self.end).normalized())
      rgb = self.image.getpixel((event.x(), event.y()))
      self.signals.mouse_moved.emit((event.x(), event.y(), *rgb))

  def mouseReleaseEvent(self, event):
    self.rubberBand.hide()
    if self.end:
      if self.origin.y() < self.end.y():
        if self.origin.x() < self.end.x():
          rect = (self.origin.x(), self.origin.y(), self.end.x(), self.end.y())
        else:
          rect = (self.end.x(), self.origin.y(), self.origin.x(), self.end.y())
      else:
        if self.origin.x() < self.end.x():
          rect = (self.origin.x(), self.end.y(), self.end.x(), self.origin.y())
        else:
          rect = (self.end.x(), self.end.y(), self.origin.x(), self.origin.y())
      crop = self.image.crop(box=rect)
      self.signals.selection_done.emit(crop)