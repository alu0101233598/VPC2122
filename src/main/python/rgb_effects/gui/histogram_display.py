
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class HistogramDisplay(QMainWindow):
  def __init__(self, histograms, title, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.tabs = QTabWidget()
    self.histograms = histograms
    self.title = title
    self.setWindowTitle(self.title + " Histograms")

    for histogram in self.histograms:
      self.tabs.addTab(FigureCanvasQTAgg(histogram), self.title)

    self.setCentralWidget(self.tabs)
    self.show()
