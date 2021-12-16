from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, \
                            QLabel, QCheckBox, QDoubleSpinBox, QMessageBox, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from math import floor

from rgb_effects.common.display_signals import DisplaySignals

class RotateDisplay(QDialog):
  def __init__(self, window, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Dialog initialization
    self.signals = DisplaySignals()
    self.window = window
    self.image_data = self.window.image_data
    self.setWindowTitle("Rotate Operation")
    qbtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(qbtn)
    buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept_and_finish)
    buttonBox.rejected.connect(self.reject)
    layout = QVBoxLayout()
    layout.setSpacing(20)
    h_layout = QHBoxLayout()

    angle_spin_label = QLabel("x rotate\n(Original width: " + str(self.image_data.width) + " pixels)")

    angle_spin_layout = QVBoxLayout()
    angle_spin_layout.addWidget(angle_spin_label)
    angle = 180.0

    self.spin = QDoubleSpinBox()
    self.spin.setMinimum(0)
    self.spin.setMaximum(360)
    self.spin.setValue(angle)

    self.check_box = QCheckBox()
    self.check_box.setText("anti-clockwise")

    h_layout.addWidget(QLabel("Angle:"))
    h_layout.addWidget(self.spin)

    box_layout = QVBoxLayout()
    box_layout.addWidget(QLabel("Interpolation"))
    self.interpolation_box = QComboBox()
    self.interpolation_box.addItem("Bilinear")
    self.interpolation_box.addItem("Nearest Neighbour")
    box_layout.addWidget(self.interpolation_box)

    layout.addLayout(h_layout)
    layout.addWidget(self.check_box)
    layout.addLayout(box_layout)
    layout.addWidget(buttonBox)
    self.setLayout(layout)

  def accept_and_finish(self):
    title = f"Rotate Function: {self.window.title}"
    checked = self.check_box.isChecked()
    angle = (1 if checked else -1) * self.spin.value()
    interpolation_method = self.interpolation_box.currentText()
    self.signals.done.emit((angle, interpolation_method, {"title": title}))
    self.accept()
