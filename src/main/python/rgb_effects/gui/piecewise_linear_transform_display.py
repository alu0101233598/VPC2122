from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QMdiArea, QComboBox, QMessageBox, QHBoxLayout, QSpinBox
from PyQt5.QtCore import Qt, pyqtSignal

from rgb_effects.common.display_signals import DisplaySignals

class PiecewiseLinearTransformDisplay(QDialog):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.signals = DisplaySignals()
    self.setWindowTitle("Piecewise Linear Transformation")
    
    qbtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(qbtn)
    buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept_and_finish)
    buttonBox.rejected.connect(self.reject)
    layout = QVBoxLayout()
    layout.setSpacing(20)
    h_layout = QHBoxLayout()

    # Linear Transformation initialization
    linear_transformation_layout = QVBoxLayout()
    linear_transformation_label = QLabel("Linear Transformation")
    linear_transformation_layout.addWidget(linear_transformation_label)

    inner_layout = QHBoxLayout()
    self.spin = QSpinBox()
    self.spin.setMinimum(1)
    self.spin.setMaximum(256)
    inner_layout.addWidget(self.spin)
    linear_transformation_layout.addLayout(inner_layout)

    h_layout.addLayout(linear_transformation_layout)

    layout.addLayout(h_layout)
    layout.addWidget(buttonBox)

    self.setLayout(layout)

  def accept_and_finish(self):
    title = f"Piecewise Linear Transformation"
    self.signals.done.emit((self.spin.value(), {"title": title}))
    self.accept()