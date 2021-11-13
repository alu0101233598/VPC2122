from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from rgb_effects.common.display_signals import DisplaySignals
from rgb_effects.gui.double_slider import DoubleSlider

spinbox_stylesheet = """
QDoubleSpinBox {{
  background: {color};
}}
"""

class GammaDisplay(QDialog):
  def __init__(self, window, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Dialog initialization
    self.signals = DisplaySignals()
    self.window = window
    self.setWindowTitle("Gamma Operation")
    qbtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(qbtn)
    buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept_and_finish)
    buttonBox.rejected.connect(self.reject)
    layout = QVBoxLayout()
    layout.setSpacing(20)
    h_layout = QHBoxLayout()

    # Gamma initialization
    if window.image_data.isGray:
      gamma_data = [{"name": "Gray", "data": 1.0, "color": "#cccccc"}]
    else:
      gamma_data = [
        {"name": "Red", "data": 1.0, "color": "#ff8787"},
        {"name": "Green", "data": 1.0, "color": "#87ff95"},
        {"name": "Blue", "data": 1.0, "color": "#8789ff"}
      ]
    gamma_layout = QVBoxLayout()
    gamma_label = QLabel("Gamma")
    gamma_layout.addWidget(gamma_label)
    self.gamma_sliders = []
    for n, band in enumerate(gamma_data):
      inner_layout = QHBoxLayout()
      slider = DoubleSlider(Qt.Horizontal)
      slider.setMinimum(0.05)
      slider.setMaximum(20.0)
      slider.setValue(float(band["data"]))
      self.gamma_sliders.append(slider)
      spin_box = QDoubleSpinBox()
      spin_box.setMinimum(0.05)
      spin_box.setMaximum(20.0)
      spin_box.setValue(float(band["data"]))
      spin_box.valueChanged.connect(slider.setValue)
      spin_box.setStyleSheet(spinbox_stylesheet.format(color=band["color"]))
      slider.doubleValueChanged.connect(spin_box.setValue)
      inner_layout.addWidget(spin_box)
      inner_layout.addWidget(slider)
      gamma_layout.addLayout(inner_layout)
    h_layout.addLayout(gamma_layout)

    layout.addLayout(h_layout)
    layout.addWidget(buttonBox)
    self.setLayout(layout)

  def accept_and_finish(self):
    title = f"Gamma Function: {self.window.title}"
    self.signals.done.emit((list(map(lambda x: x.value(), self.gamma_sliders)), {"title": title}))
    self.accept()