
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

    colors = ['Gray'] if len(self.histograms) == 2 else ['Red', 'Green', 'Blue']
    i = 0
    for histogram in self.histograms:
      tag = colors[i % len(colors)] + (" Cumulative" if int(i / len(colors)) == 1 else "")
      self.tabs.addTab(FigureCanvasQTAgg(histogram), tag)
      i += 1 if i < len(self.histograms) else - i

    self.setCentralWidget(self.tabs)
    self.show()
