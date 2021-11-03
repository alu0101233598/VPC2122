from PyQt5.QtWidgets import QLabel, QWidget, QRubberBand
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QRect, QSize

class ImageLabel(QLabel):
  mouse_moved = pyqtSignal(tuple)

  def __init__(self, image, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.image =  image
    self.rubberBand = None
    data = image.tobytes("raw", "RGB")
    qimage = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
    self.setMouseTracking(True)
    self.setPixmap(pixmap)

  def mousePressEvent(self, event):
    self.origin = event.pos()
    if not self.rubberBand:
      self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
    self.rubberBand.setGeometry(QRect(self.origin, QSize()))
    self.rubberBand.show()
    
  def mouseMoveEvent(self, event):
    if event.x() < self.image.width and event.y() < self.image.height:
      if self.rubberBand:
        self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
      rgb = self.image.getpixel((event.x(), event.y()))
      self.mouse_moved.emit((event.x(), event.y(), *rgb))

  def mouseReleaseEvent(self, event):
    self.rubberBand.hide()