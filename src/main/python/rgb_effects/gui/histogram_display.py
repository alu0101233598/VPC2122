
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import io
from PIL import Image
import matplotlib.pyplot as plt

alpha = 1.1

switchColorCode = {
  0: [(x / (255 * alpha), x / (255 * alpha), x / (255 * alpha)) for x in range(256)],
  1: [(x / 255, 0, 0) for x in range(256)],
  2: [(0, x / 255, 0) for x in range(256)],
  3: [(0, 0, x / 255) for x in range(256)]
}

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

def createHistogram(self, image, cumulative):
  data = image.image_data
  if cumulative:
    planes = [data.rCumHistogram] if data.isGray else [data.rCumHistogram, data.gCumHistogram, data.bCumHistogram]
  else:
    planes = [data.rHistogram] if data.isGray else [data.rHistogram, data.gHistogram, data.bHistogram]
  colors = ['black', 'red', 'green', 'blue']
  i = 0 if data.isGray else 1
  switchMean = {
    0: data.rBrightness,
    1: data.rBrightness,
    2: data.gBrightness,
    3: data.bBrightness
  }
  switchRange = {
    0: data.rRange,
    1: data.rRange,
    2: data.gRange,
    3: data.bRange
  }

  histograms = []

  for plane in planes:
    label = QLabel(self, alignment=Qt.AlignCenter)
    fig = plt.figure(figsize=(15, 10), dpi=80)
    
    plt.bar(range(len(plane)), plane, color=switchColorCode[i], width = 1)
    
    mean = switchMean[i]
    plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
    min_ylim, max_ylim = plt.ylim()
    min_xlim, max_xlim = plt.xlim()
    plt.text(mean*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean), fontsize=20)
    plt.text(max_xlim*0.8, max_ylim*0.95, ('Effective ' if cumulative else '') + 'Range: {0}'.format(list(switchRange[i])), fontsize=15)

    histograms.append(fig)
    i += 1
  
  return histograms
