import sys, os, re

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QImage, QKeySequence
from PyQt5.QtCore import Qt, QThreadPool

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PIL.ImageQt import ImageQt
from PIL import Image

from rgb_effects.gui.image_display import ImageDisplay
from rgb_effects.gui.histogram_display import createHistogram, HistogramDisplay
from rgb_effects.gui.information_display import InformationDisplay
from rgb_effects.gui.brightness_contrast_display import BrightnessContrastDisplay
from rgb_effects.gui.difference_display import DifferenceDisplay
from rgb_effects.gui.histogram_specification_display import HistogramSpecificationDisplay
from rgb_effects.gui.linear_transform_display import LinearTransformDisplay
from rgb_effects.gui.gamma_display import GammaDisplay
from rgb_effects.model.image_data import ImageData
from rgb_effects.operation import grayscale, brightness_contrast, difference, histogram_specification, equalization, gamma, linear_transform, negative

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
    self.progressBar = QProgressBar()
    self.statusBar().addPermanentWidget(self.progressBar)
    self.progressBar.hide()
    self.loadImageSignal = None
    self.loadImageWindow = None
 
    self.mdi = QMdiArea()
    self.setCentralWidget(self.mdi)
    self.counter = 1
    self.threadpool = QThreadPool()
    self.histogramDisplays = []
    self.informationDisplays = []

  def createActions(self):
    # File menu
    self.openAction = QAction("&Open", self)
    self.openAction.triggered.connect(self.openFileNameDialog)
    self.openAction.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_O))
    self.saveAction = QAction("&Save", self)
    self.saveAction.triggered.connect(self.saveFileDialog)
    self.saveAction.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
    self.exitAction = QAction("&Exit", self)
    self.exitAction.triggered.connect(qApp.quit)
    # Edit menu
    self.informationAction = QAction("&Image information")
    self.informationAction.triggered.connect(self.informationDialog)
    self.histogramsAction = QAction("&Histograms", self)
    self.histogramsAction.triggered.connect(self.histogramsDialog)
    self.histogramsAction.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_H))
    self.duplicateAction = QAction("&Duplicate", self)
    self.duplicateAction.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_D))
    self.duplicateAction.triggered.connect(self.duplicateImage)
    # Images menu
    self.grayscaleAction = QAction("&Grayscale conversion")
    self.grayscaleAction.triggered.connect(lambda: self.applyOperation(grayscale.NTSC_conversion))
    self.grayscaleAction.setShortcut(QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_G))
    self.negativeAction = QAction("&Negative")
    self.negativeAction.triggered.connect(lambda: self.applyOperation(negative.apply))
    self.linearTransformAction = QAction("Segmented &linear transformation")
    self.linearTransformAction.triggered.connect(
      lambda: self.applyOperationDialog(LinearTransformDisplay, linear_transform.apply)
    )
    self.brightnessContrastAction = QAction("&Brightness / Contrast")
    self.brightnessContrastAction.triggered.connect(
      lambda: self.applyOperationDialog(BrightnessContrastDisplay, brightness_contrast.apply_transformation)
    )
    self.histogramEqAction = QAction("Histogram &equalization")
    self.histogramEqAction.triggered.connect(lambda: self.applyOperation(equalization.apply))
    self.histogramSpecAction = QAction("Histogram &specification")
    self.histogramSpecAction.triggered.connect(
      lambda: self.applyOperationDialog(HistogramSpecificationDisplay, histogram_specification.apply)
    )
    self.gammaAction = QAction("Ga&mma correction")
    self.gammaAction.triggered.connect(
      lambda: self.applyOperationDialog(GammaDisplay, gamma.apply)
    )
    self.imageDiferenceAction = QAction("Image &diference")
    self.imageDiferenceAction.triggered.connect(
      lambda: self.applyOperationDialog(DifferenceDisplay, difference.calculate_absolute_difference)
    )
    self.changesAction = QAction("&Changes")
    # self.changesAction.triggered.connect()

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
    editMenu.addAction(self.informationAction)
    editMenu.addAction(self.histogramsAction)
    editMenu.addSeparator()
    editMenu.addAction(self.duplicateAction)
    # Images menu
    imageMenu = menuBar.addMenu("&Operation")
    imageMenu.addSeparator()
    imageMenu.addAction(self.grayscaleAction)
    imageMenu.addAction(self.negativeAction)
    imageMenu.addAction(self.linearTransformAction)
    imageMenu.addAction(self.brightnessContrastAction)
    imageMenu.addSeparator()
    imageMenu.addAction(self.histogramEqAction)
    imageMenu.addAction(self.histogramSpecAction)
    imageMenu.addAction(self.gammaAction)
    imageMenu.addAction(self.imageDiferenceAction)
    imageMenu.addAction(self.changesAction)
    # Help menu
    helpMenu = menuBar.addMenu("&Help")
    helpMenu.addAction(self.helpContentAction)
    helpMenu.addAction(self.aboutAction)

  def createMDIImage(self, title, image):
    bare_title = re.sub(r'\(\d+\)\s*', '', title)
    formatted_title = f"({self.counter}) {bare_title}"
    sub = ImageDisplay(image, formatted_title, self.threadpool)
    self.counter += 1
    sub.signals.mouse_moved.connect(self.updateStatusBar)
    sub.signals.selection_done.connect(lambda crop: self.createMDIImage(title, crop))
    if self.loadImageSignal:
      self.loadImageWindow.disconnect(self.loadImageSignal)
    self.loadImageSignal = sub.signals.progress.connect(self.manageProgressBar)
    self.loadImageWindow = sub
    self.mdi.addSubWindow(sub)
    sub.show()

  def updateStatusBar(self, info):
    x, y, r, g, b = info[:5]
    self.statusBar().showMessage(f"({x}, {y}) R: {r} / G: {g} / B: {b}")

  def openFileNameDialog(self):
    path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", f"{self.ctx.get_resource(EXAMPLES_DIR)}", "All Files (*)")
    if path:
      print('Opening ' + path)
      image = Image.open(path, 'r')
      fileName = os.path.basename(path)
      self.createMDIImage(fileName, image)

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
        QMessageBox.information(self, "Help", f"Nothing to save!")

  def duplicateImage(self):
    sub = self.mdi.activeSubWindow()
    if sub:
      self.createMDIImage(sub.title, sub.image)

  def getActiveWindow(self):
    sub = self.mdi.activeSubWindow()
    if sub:
      if sub.image_data:
        return sub
      else:
        QMessageBox.information(self, "Help", "The picture is being processed, please wait.")
    else:
      QMessageBox.information(self, "Help", "No picture selected!")

  def histogramsDialog(self):
    image = self.getActiveWindow()
    if image:
      histograms = []
      for cumulative in [False, True]:
        histograms += createHistogram(self, image, cumulative)
      self.histogramDisplays.append(HistogramDisplay(histograms, image.title, parent=self))
      
  def informationDialog(self):
    imageSubWin = self.getActiveWindow()
    if imageSubWin:
      self.informationDisplays.append(InformationDisplay(imageSubWin))
    
  def applyOperationDialog(self, dialog_class, op_callback):
    if not dialog_class:
      raise "Dialog is missing!"
    sub = self.getActiveWindow()
    if sub:
      dialog = dialog_class(sub)
      dialog.signals.done.connect(lambda x: self.applyOperation(op_callback, x))
      dialog.exec()

  def applyOperation(self, op_callback, param = None):
    if not op_callback:
      raise "Operation callback not defined!"
    sub = self.getActiveWindow()
    if sub:
      title = sub.title
      if param:
        if type(param[-1]) is dict and "title" in param[-1]:
          title = param[-1]["title"]
        result_image = op_callback(sub.image_data, param)
      else:
        result_image = op_callback(sub.image_data)
      self.createMDIImage(title, result_image)

  def manageProgressBar(self, progress):
    if not self.progressBar.isVisible():
      self.progressBar.show()
    self.progressBar.setValue(progress)
    if progress == 100:
      self.progressBar.reset()
      self.progressBar.hide()
      self.loadImageSignal = self.loadImageWindow = None

def run():
  appctx = ApplicationContext()
  app = MainWindow(appctx)
  sys.exit(appctx.app.exec_())