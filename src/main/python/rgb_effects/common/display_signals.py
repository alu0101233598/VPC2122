from PyQt5.QtCore import pyqtSignal, QObject

class DisplaySignals(QObject):
  done = pyqtSignal(tuple)