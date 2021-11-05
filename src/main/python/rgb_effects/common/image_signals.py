from PyQt5.QtCore import pyqtSignal, QObject

class ImageSignals(QObject):
  mouse_moved = pyqtSignal(tuple)
  selection_done = pyqtSignal(object)
  progress = pyqtSignal(int)