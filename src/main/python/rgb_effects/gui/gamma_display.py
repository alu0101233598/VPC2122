from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QSpinBox, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from rgb_effects.common.display_signals import DisplaySignals

spinbox_stylesheet = """
QSpinBox {{
  background: {color};
}}
"""

class GammaDisplay(QDialog):
  def __init__(self, window, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Dialog initialization
    self.signals = DisplaySignals()
    self.window = window
    qbtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(qbtn)
    buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept_and_finish)
    buttonBox.rejected.connect(self.reject)
    layout = QVBoxLayout()
    layout.setSpacing(20)
    h_layout = QHBoxLayout()

    # Gamma initialization
    if window.image_data.isGray:
      gamma_data = [{"name": "Gray", "data": 1, "color": "#cccccc"}]
    else:
      gamma_data = [
        {"name": "Red", "data": 1, "color": "#ff8787"},
        {"name": "Green", "data": 1, "color": "#87ff95"},
        {"name": "Blue", "data": 1, "color": "#8789ff"}
      ]
    gamma_layout = QVBoxLayout()
    gamma_label = QLabel("Gamma")
    gamma_layout.addWidget(gamma_label)
    self.gamma_sliders = []
    for n, band in enumerate(gamma_data):
      inner_layout = QHBoxLayout()
      slider = QSlider(Qt.Horizontal)
      slider.setMinimum(5)
      slider.setMaximum(2000)
      slider.setValue(int(round(band["data"])))
      self.gamma_sliders.append(slider)
      spin_box = QSpinBox()
      spin_box.setMinimum(5)
      spin_box.setMaximum(2000)
      spin_box.setValue(int(round(band["data"])))
      spin_box.valueChanged.connect(slider.setValue)
      spin_box.setStyleSheet(spinbox_stylesheet.format(color=band["color"]))
      slider.valueChanged.connect(spin_box.setValue)
      inner_layout.addWidget(spin_box)
      inner_layout.addWidget(slider)
      gamma_layout.addLayout(inner_layout)
    h_layout.addLayout(gamma_layout)

    layout.addLayout(h_layout)
    layout.addWidget(buttonBox)
    self.setLayout(layout)

  def accept_and_finish(self):
    title = f"Gamma Function: {self.window.title}"
    self.signals.done.emit((self.window.image_data, list(map(lambda x: x.value() / 100, self.gamma_sliders)), {"title": title}))
    self.accept()