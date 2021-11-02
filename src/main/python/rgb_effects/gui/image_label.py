from PyQt5.QtWidgets import QLabel

class ImageLabel(QLabel):
  def __init__(self, pixmap, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setMouseTracking(True)
    self.setPixmap(pixmap)
    
  def mouseMoveEvent(self, event):
    print(event.x(), event.y())