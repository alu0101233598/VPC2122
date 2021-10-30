from PyQt5.QtWidgets import QMdiSubWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from PIL.ImageQt import ImageQt

from rgb_effects.model.image_data import ImageData
from rgb_effects.common.worker import Worker

class ImageDisplay(QMdiSubWindow):
  def __init__(self, image, title, threadpool):
    super().__init__()
    self.image = image
    self.title = title
    self.threadpool = threadpool
    self.setWindowTitle(self.title)
    qimage = ImageQt(self.image)
    pixmap = QPixmap.fromImage(qimage)
    label = QLabel(self, alignment=Qt.AlignCenter)
    label.setMouseTracking(True)
    label.setPixmap(pixmap)
    self.setWidget(label)
    
    self.image_data = None
    worker = Worker(self.process_image)
    worker.signals.finished.connect(self.test)
    self.threadpool.start(worker)
    
  def process_image(self, **kwargs):
    self.image_data = ImageData(self.image)

  def test(self):
    from PyQt5.QtWidgets import QMessageBox
    QMessageBox.about(self, "Done!", f"Done loading {self.title}!")