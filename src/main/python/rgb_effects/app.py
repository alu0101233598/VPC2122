import sys, os

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PIL.ImageQt import ImageQt
from PIL import Image

from rgb_effects.common import utils
from rgb_effects.gui.image_display import ImageDisplay
from rgb_effects.model.image_data import ImageData

# Global variables
APP_NAME = "RGB_Effects"
ICON_NAME = "icon.png"
EXAMPLES_DIR = "examples"

class MainWindow(QMainWindow):
  def __init__(self, ctx):
    super().__init__()
    self.ctx = ctx
    self.createActions()
    self.createMenuBar()
 
    self.setWindowTitle(APP_NAME)
    icon_path = self.ctx.get_resource(ICON_NAME)
    self.setWindowIcon(QIcon(icon_path))
    self.setGeometry(0, 0, 400, 300)
    self.showMaximized()
    self.mdi = QMdiArea()
    self.setCentralWidget(self.mdi)

  def createActions(self):
    self.openAction = QAction("&Open", self)
    self.openAction.triggered.connect(self.openFileNameDialog)

    self.saveAction = QAction("&Save", self)
    self.saveAction.triggered.connect(self.saveFileDialog)

    self.exitAction = QAction("&Exit", self)
    self.exitAction.triggered.connect(qApp.quit)

    self.copyAction = QAction("&Copy", self)
    self.pasteAction = QAction("&Paste", self)
    self.cutAction = QAction("C&ut", self)

    self.helpContentAction = QAction("&Help Content", self)
    self.aboutAction = QAction("&About", self)

  def createMenuBar(self):
    menuBar = self.menuBar()
    # File menu
    fileMenu = QMenu("&File", self)
    menuBar.addMenu(fileMenu)
    fileMenu.addAction(self.openAction)
    fileMenu.addAction(self.saveAction)
    fileMenu.addAction(self.exitAction)
    # Edit menu
    editMenu = menuBar.addMenu("&Edit")
    editMenu.addAction(self.copyAction)
    editMenu.addAction(self.pasteAction)
    editMenu.addAction(self.cutAction)
    # Images menu
    imageMenu = menuBar.addMenu("&Images")
    # Help menu
    helpMenu = menuBar.addMenu("&Help")
    helpMenu.addAction(self.helpContentAction)
    helpMenu.addAction(self.aboutAction)

  def createMDIImage(self, path):
    image = Image.open(path, 'r')
    fileName = os.path.basename(path)
    sub = ImageDisplay(image, fileName)
    self.mdi.addSubWindow(sub)
    sub.show()

  def createMDIHistogram(self, image, cumulative):
    planes = [image.r] if image.isBw else [image.r, image.g, image.b]
    colors = ['black', 'red', 'green', 'blue']
    i = 0 if image.isBw else 1
    switchMean = {
      0: image.rBrightness,
      1: image.rBrightness,
      2: image.bBrightness,
      3: image.gBrightness
    }
    switchRange = {
      0: image.rRange,
      1: image.rRange,
      2: image.bRange,
      3: image.gRange
    }

    for plane in planes:
      label = QLabel(self, alignment=Qt.AlignCenter)
      fig = plt.figure(figsize=(15, 10), dpi=80)
      
      n, bins, patches = plt.hist(tuple(plane), cumulative=cumulative, bins=256, facecolor='#2ab0ff', edgecolor='#000000', linewidth=0.1, alpha=0.7)
      n = n.astype('int')
      for j in range(len(patches)):
        patches[j].set_facecolor(utils.switchColorCode[i][j])
      
      mean = switchMean[i]
      plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
      min_ylim, max_ylim = plt.ylim()
      min_xlim, max_xlim = plt.xlim()
      plt.text(mean*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(mean), fontsize=20)
      plt.text(max_xlim*0.8, max_ylim*0.95, 'Range: {0}'.format(list(switchRange[i])), fontsize=15)
      histogramImage = utils.fig2img(fig)

      label.setPixmap(QPixmap.fromImage(ImageQt(histogramImage)))
      sub = QMdiSubWindow()
      sub.setWidget(label)
      cummuString = ' (cumulative)' if cumulative else ''
      sub.setWindowTitle(f"Histogram [{colors[i]}]{cummuString} - {image.fileName}")
      self.mdi.addSubWindow(sub)
      sub.show()
      i += 1

  def openFileNameDialog(self):
    fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", f"{self.ctx.get_resource(EXAMPLES_DIR)}", "All Files (*);;Python Files (*.py)")
    if fileName:
      print('Opening ' + fileName)
      self.createMDIImage(fileName)
      # for cumulative in [False, True]:
      #   self.createMDIHistogram(image, cumulative)

  def saveFileDialog(self):
    fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "All Files (*);;Text Files (*.txt)")
    if fileName:
      print(fileName)


def run():
  appctx = ApplicationContext()
  app = MainWindow(appctx)
  sys.exit(appctx.app.exec_())