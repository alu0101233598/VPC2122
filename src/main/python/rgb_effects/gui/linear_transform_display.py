from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QMdiArea, QComboBox, QMessageBox, QHBoxLayout, QSpinBox
from PyQt5.QtCore import Qt, pyqtSignal

from rgb_effects.common.display_signals import DisplaySignals
from rgb_effects.gui.piecewise_linear_transform_display import PiecewiseLinearTransformDisplay
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class LinearTransformDisplay(QDialog):
  def __init__(self, window, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.signals = DisplaySignals()
    self.windows = window
    self.setAttribute(Qt.WA_DeleteOnClose)
    self.setWindowTitle("Linear Transformation")

    d = PiecewiseLinearTransformDisplay()
    d.signals.done.connect(self.define_linear_transformation)
    d.rejected.connect(self.reject)
    d.exec()

  def define_linear_transformation(self, return_piecewise):
    nPoints = return_piecewise[0] + 1
    self.points = [[0, 0] for i in range(nPoints)]
    self.layout = QHBoxLayout()
    self.layout.setAlignment(Qt.AlignCenter)
    self.layout.setSpacing(20)

    qbtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(qbtn)
    buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept_and_finish)
    buttonBox.rejected.connect(self.reject)
    self.fig = plt.figure()
    self.clear_fig()

    v_layout = QVBoxLayout()
    v_layout.setAlignment(Qt.AlignCenter)
    for i in range(nPoints):
      h_layout = QHBoxLayout()
      
      h_layout.addWidget(QLabel("Point: "))
      spin = QSpinBox()
      spin.setMinimum(0)
      spin.setMaximum(255)
      spin.valueChanged.connect(
        lambda spin_value = spin.value(), val = i: self.actualize_plot(spin_value, val, 0)
      )
      h_layout.addWidget(spin)

      h_layout.addWidget(QLabel("Value: "))
      spin2 = QSpinBox()
      spin2.setMinimum(0)
      spin2.setMaximum(255)
      spin2.valueChanged.connect(
        lambda spin_value = spin2.value(), val = i: self.actualize_plot(spin_value, val, 1)
      )
      h_layout.addWidget(spin2)

      h_layout.setAlignment(Qt.AlignCenter)
      v_layout.addLayout(h_layout)

    v_layout.addWidget(buttonBox)
    self.layout.addLayout(v_layout)
    self.figWid = FigureCanvasQTAgg(self.fig)
    self.layout.addWidget(self.figWid)

    self.setLayout(self.layout)

  def accept_and_finish(self):
    title = f"Linear Transformation"
    for i in range(len(self.points) - 1):
      if self.points[i][0] >= self.points[i + 1][0]:
        QMessageBox.critical(self, "Operation failed", "Invalid linear " + \
            "transformation\n" + "x in pi " + str(self.points[i]) + \
                " <= x in pf " + str(self.points[i + 1]))
        return
    self.signals.done.emit((self.points, {"title": title}))
    self.accept()

  def actualize_plot(self, spin_value, i, j):
    self.clear_fig()
    self.points[i][j] = spin_value
    x = []
    y = []
    for k in range(len(self.points)):
      x.append(self.points[k][0])
      y.append(self.points[k][1])
    plt.plot(x, y)
    self.figWid.draw()

  def clear_fig(self):
    self.fig.clear()
    plt.xlim(0, 255)
    plt.ylim(0, 255)
    plt.xlabel('Input Image')
    plt.ylabel('Output Image')
