import sys, os, re

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QImage, QKeySequence
from PyQt5.QtCore import Qt, QThreadPool

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
    self.setWindowTitle(APP_NAME)
    icon_path = self.ctx.get_resource(ICON_NAME)
    self.setWindowIcon(QIcon(icon_path))
    self.setGeometry(0, 0, 400, 300)
    self.showMaximized()
    self.createActions()
    self.createMenuBar()
    self.setStatusBar(QStatusBar(self))
 
    self.mdi = QMdiArea()
    self.setCentralWidget(self.mdi)
    self.threadpool = QThreadPool()

  def createActions(self):
    # File menu
    self.openAction = QAction("&Open", self)
    self.openAction.triggered.connect(self.openFileNameDialog)
    self.saveAction = QAction("&Save", self)
    self.saveAction.triggered.connect(self.saveFileDialog)
    self.exitAction = QAction("&Exit", self)
    self.exitAction.triggered.connect(qApp.quit)
    # Edit menu
    self.duplicateAction = QAction("&Duplicate", self)
    self.duplicateAction.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_D))
    self.duplicateAction.triggered.connect(self.duplicateImage)
    # Images menu
    self.histogramsAction = QAction("&Histograms", self)
    self.histogramsAction.triggered.connect(self.histogramsDialog)

    # TODO: help menu
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
    editMenu.addAction(self.histogramsAction)
    editMenu.addAction(self.duplicateAction)
    # Images menu
    imageMenu = menuBar.addMenu("&Operation")
    # Help menu
    helpMenu = menuBar.addMenu("&Help")
    helpMenu.addAction(self.helpContentAction)
    helpMenu.addAction(self.aboutAction)

  def createMDIImage(self, title, image):
    sub = ImageDisplay(image, title, self.threadpool)
    sub.signals.mouse_moved.connect(self.updateStatusBar)
    sub.signals.selection_done.connect(lambda crop: self.createMDIImage(title, crop))
    self.mdi.addSubWindow(sub)
    sub.show()

  def updateStatusBar(self, info):
    x, y, r, g, b = info[:5]
    self.statusBar().showMessage(f"({x}, {y}) R: {r} / G: {g} / B: {b}")


  def createMDIHistogram(self, image, cumulative):
    data = image.image_data
    if cumulative:
      planes = [data.rAccHistogram] if data.isGray else [data.rAccHistogram, data.gAccHistogram, data.bAccHistogram]
    else:
      planes = [data.rHistogram] if data.isGray else [data.rHistogram, data.gHistogram, data.bHistogram]
    colors = ['black', 'red', 'green', 'blue']
    i = 0 if data.isGray else 1
    switchMean = {
      0: data.rBrightness,
      1: data.rBrightness,
      2: data.bBrightness,
      3: data.gBrightness
    }
    switchRange = {
      0: data.rRange,
      1: data.rRange,
      2: data.bRange,
      3: data.gRange
    }

    for plane in planes:
      label = QLabel(self, alignment=Qt.AlignCenter)
      fig = plt.figure(figsize=(15, 10), dpi=80)
      
      plt.bar(range(len(plane)), plane, color=utils.switchColorCode[i], width = 1)
      
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
      sub.setWindowTitle(f"Histogram [{colors[i]}]{cummuString} - {image.title}")
      self.mdi.addSubWindow(sub)
      sub.show()
      i += 1

  def openFileNameDialog(self):
    fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", f"{self.ctx.get_resource(EXAMPLES_DIR)}", "All Files (*)")
    if fileName:
      print('Opening ' + fileName)
      self.createMDIImage(fileName)

  def saveFileDialog(self):
    activeSubWindow = self.mdi.activeSubWindow()
    fileName, fileFormat = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", f"{self.ctx.get_resource(EXAMPLES_DIR)}", "PNG (*.png)")
    if fileName:
      fileFormat = re.findall(r"(?<=\.)\w+", fileFormat)[0]
      if fileName.split('.')[-1] != fileFormat:
        fileName += "." + fileFormat
      if activeSubWindow:
        print("Saving " + fileName)
        activeSubWindow.image.save(fileName, format=fileFormat)
      else:
        print("Nothing to save")

  def duplicateImage(self):
    sub = self.mdi.activeSubWindow()
    if sub:
      self.createMDIImage(sub.title, sub.image)

  def histogramsDialog(self):
    image = self.mdi.activeSubWindow()
    if image:
      for cumulative in [False, True]:
        self.createMDIHistogram(image, cumulative)
    else:
      print("Nothing selected!")

def run():
  appctx = ApplicationContext()
  app = MainWindow(appctx)
  sys.exit(appctx.app.exec_())