from PyQt5.QtWidgets import QMdiSubWindow, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

from PIL.ImageQt import ImageQt

from rgb_effects.gui.image_label import ImageLabel
from rgb_effects.model.image_data import ImageData
from rgb_effects.common.worker import Worker

class ImageDisplay(QMdiSubWindow):
  def __init__(self, image, title, threadpool):
    super().__init__()
    self.image = image
    self.title = title
    self.threadpool = threadpool
    self.setWindowTitle(self.title)
    data = self.image.convert("RGB").tobytes("raw", "RGB")
    qimage = QImage(data, self.image.size[0], self.image.size[1], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
    label = ImageLabel(pixmap, self, alignment=Qt.AlignCenter)
    super().setWidget(label)
    self.setFixedSize(pixmap.width(), pixmap.height())
    
    self.image_data = None
    worker = Worker(self.process_image)
    worker.signals.error.connect(self.load_error)
    worker.signals.finished.connect(self.test)
    self.threadpool.start(worker)
    
  def process_image(self, **kwargs):
    self.image_data = ImageData(self.image)

  def load_error(self, e):
    QMessageBox.critical(self, "Error", f"Error loading {self.title}")
    super().close()

  def test(self):
    QMessageBox.about(self, "Done!", f"Done loading {self.title}!")