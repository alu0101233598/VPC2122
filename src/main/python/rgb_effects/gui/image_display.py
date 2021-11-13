from PyQt5.QtWidgets import QMdiSubWindow, QLabel, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSignal

from PIL.ImageQt import ImageQt

from rgb_effects.common.image_signals import ImageSignals
from rgb_effects.gui.image_label import ImageLabel
from rgb_effects.model.image_data import ImageData
from rgb_effects.common.worker import Worker

class ImageDisplay(QMdiSubWindow):
  def __init__(self, image, title, threadpool):
    super().__init__()
    self.signals = ImageSignals()
    self.image = image.convert("RGBA")
    self.title = title
    self.threadpool = threadpool
    self.setWindowTitle(self.title)
    self.setAttribute(Qt.WA_DeleteOnClose)
    
    label = ImageLabel(self.image, self, alignment=Qt.AlignCenter)
    label.signals.mouse_moved.connect(self.propagate_mouse_moved)
    label.signals.selection_done.connect(self.propagate_selection_done)
    layout = QVBoxLayout()
    w = QWidget()
    layout.addWidget(label)
    layout.setAlignment(Qt.AlignCenter)
    w.setLayout(layout)
    self.setWidget(w)
    
    self.image_data = None
    worker = Worker(self.process_image)
    worker.signals.error.connect(self.load_error)
    worker.signals.progress.connect(self.propagate_progress)
    self.threadpool.start(worker)
    
  def process_image(self, **kwargs):
    self.image_data = ImageData(self.image, **kwargs)

  def load_error(self, e):
    QMessageBox.critical(self, "Error", f"Error loading {self.title}")
    super().close()

  def propagate_mouse_moved(self, info):
    self.signals.mouse_moved.emit(info)

  def propagate_selection_done(self, crop):
    self.signals.selection_done.emit(crop)

  def propagate_progress(self, progress):
    self.signals.progress.emit(progress)