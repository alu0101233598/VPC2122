from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, \
                            QLabel, QSpinBox, QDoubleSpinBox, QMessageBox, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from math import floor

from rgb_effects.common.display_signals import DisplaySignals

spinbox_stylesheet = """
QDoubleSpinBox {{
  background: {color};
}}
"""

class ScaleDisplay(QDialog):
  def __init__(self, window, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Dialog initialization
    self.signals = DisplaySignals()
    self.window = window
    self.image_data = self.window.image_data
    self.setWindowTitle("Scale Operation")
    qbtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(qbtn)
    buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept_and_finish)
    buttonBox.rejected.connect(self.reject)
    layout = QVBoxLayout()
    layout.setSpacing(20)
    h_layout = QHBoxLayout()

    x_scale_label = QLabel("x scale\n(Original width: " + str(self.image_data.width) + " pixels)")
    y_scale_label = QLabel("y scale\n(Original height: " + str(self.image_data.height) + " pixels)")

    x_scale_layout = QVBoxLayout()
    x_scale_layout.addWidget(x_scale_label)
    self.x_scale = 100.0

    x_inner_layout_1 = QHBoxLayout()
    self.x_spin_box_1 = QDoubleSpinBox()
    self.x_spin_box_1.setMinimum(1)
    self.x_spin_box_1.setMaximum(100 * self.image_data.width)
    self.x_spin_box_1.setValue(self.x_scale * self.image_data.width / 100)

    x_inner_layout_2 = QHBoxLayout()
    self.x_spin_box_2 = QDoubleSpinBox()
    self.x_spin_box_2.setMinimum(0.01)
    self.x_spin_box_2.setMaximum(10000)
    self.x_spin_box_2.setValue(self.x_scale)

    self.x_spin_box_1.valueChanged.connect(self.x_rescale_and_set_value_1)
    self.x_spin_box_2.valueChanged.connect(self.x_rescale_and_set_value_2)

    x_inner_layout_1.addWidget(self.x_spin_box_1)
    x_inner_layout_1.addWidget(QLabel("Pixels"))
    x_inner_layout_2.addWidget(self.x_spin_box_2)
    x_inner_layout_2.addWidget(QLabel("%"))
    x_scale_layout.addLayout(x_inner_layout_1)
    x_scale_layout.addLayout(x_inner_layout_2)

    h_layout.addLayout(x_scale_layout)

    y_scale_layout = QVBoxLayout()
    y_scale_layout.addWidget(y_scale_label)
    self.y_scale = 100.0

    y_inner_layout_1 = QHBoxLayout()
    self.y_spin_box_1 = QDoubleSpinBox()
    self.y_spin_box_1.setMinimum(1)
    self.y_spin_box_1.setMaximum(100 * self.image_data.height)
    self.y_spin_box_1.setValue(self.y_scale * self.image_data.height / 100)

    y_inner_layout_2 = QHBoxLayout()
    self.y_spin_box_2 = QDoubleSpinBox()
    self.y_spin_box_2.setMinimum(0.01)
    self.y_spin_box_2.setMaximum(10000)
    self.y_spin_box_2.setValue(self.y_scale)

    self.y_spin_box_1.valueChanged.connect(self.y_rescale_and_set_value_1)
    self.y_spin_box_2.valueChanged.connect(self.y_rescale_and_set_value_2)

    y_inner_layout_1.addWidget(self.y_spin_box_1)
    y_inner_layout_1.addWidget(QLabel("Pixels"))
    y_inner_layout_2.addWidget(self.y_spin_box_2)
    y_inner_layout_2.addWidget(QLabel("%"))
    y_scale_layout.addLayout(y_inner_layout_1)
    y_scale_layout.addLayout(y_inner_layout_2)

    h_layout.addLayout(y_scale_layout)

    box_layout = QVBoxLayout()
    self.interpolation_box = QComboBox()
    self.interpolation_box.addItem("Bilinear")
    self.interpolation_box.addItem("Nearest Neighbour")
    box_layout.addWidget(QLabel("Interpolation"))
    box_layout.addWidget(self.interpolation_box)

    layout.addLayout(h_layout)
    layout.addLayout(box_layout)
    layout.addWidget(buttonBox)
    self.setLayout(layout)

  def accept_and_finish(self):
    title = f"Scale Function: {self.window.title}"
    x_scale_factor = self.x_scale / 100
    y_scale_factor = self.y_scale / 100
    interpolation_method = self.interpolation_box.currentText()
    self.signals.done.emit((x_scale_factor, y_scale_factor, interpolation_method, {"title": title}))
    self.accept()

  def x_rescale_and_set_value_1(self, value):
    if self.x_scale != value / self.image_data.width * 100:
      self.x_scale = value / self.image_data.width * 100
      self.x_spin_box_2.setValue(self.x_scale)

  def x_rescale_and_set_value_2(self, value):
    if self.x_scale != value:
      self.x_scale = value
      self.x_spin_box_1.setValue(self.x_scale * self.image_data.width / 100)

  def y_rescale_and_set_value_1(self, value):
    if self.y_scale != value / self.image_data.height * 100:
      self.y_scale = value / self.image_data.height * 100
      self.y_spin_box_2.setValue(self.y_scale)

  def y_rescale_and_set_value_2(self, value):
    if self.y_scale != value:
      self.y_scale = value
      self.y_spin_box_1.setValue(self.y_scale * self.image_data.height / 100)