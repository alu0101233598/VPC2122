from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QSpinBox, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from rgb_effects.common.display_signals import DisplaySignals

spinbox_stylesheet = """
QSpinBox {{
  background: {color};
}}
"""

class BrightnessContrastDisplay(QDialog):
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

    # Brightness initialization
    if window.image_data.isGray:
      brightness_data = [{"name": "Gray", "data": window.image_data.rBrightness, "color": "#cccccc"}]
    else:
      brightness_data = [
        {"name": "Red", "data": window.image_data.rBrightness, "color": "#ff8787"},
        {"name": "Green", "data": window.image_data.gBrightness, "color": "#87ff95"},
        {"name": "Blue", "data": window.image_data.bBrightness, "color": "#8789ff"}
      ]
    brightness_layout = QVBoxLayout()
    brightness_label = QLabel("Brightness")
    brightness_layout.addWidget(brightness_label)
    self.brightness_sliders = []
    for n, band in enumerate(brightness_data):
      inner_layout = QHBoxLayout()
      slider = QSlider(Qt.Horizontal)
      slider.setMinimum(0)
      slider.setMaximum(255)
      slider.setValue(band["data"])
      self.brightness_sliders.append(slider)
      spin_box = QSpinBox()
      spin_box.setMinimum(0)
      spin_box.setMaximum(255)
      spin_box.setValue(band["data"])
      spin_box.valueChanged.connect(slider.setValue)
      spin_box.setStyleSheet(spinbox_stylesheet.format(color=band["color"]))
      slider.valueChanged.connect(spin_box.setValue)
      inner_layout.addWidget(spin_box)
      inner_layout.addWidget(slider)
      brightness_layout.addLayout(inner_layout)
    h_layout.addLayout(brightness_layout)

    # Contrast initialization
    if window.image_data.isGray:
      contrast_data = [{"name": "Gray", "data": window.image_data.rContrast, "color": "#cccccc"}]
    else:
      contrast_data = [
        {"name": "Red", "data": window.image_data.rContrast, "color": "#ff8787"},
        {"name": "Green", "data": window.image_data.gContrast, "color": "#87ff95"},
        {"name": "Blue", "data": window.image_data.bContrast, "color": "#8789ff"}
      ]
    contrast_layout = QVBoxLayout()
    contrast_label = QLabel("Contrast")
    contrast_layout.addWidget(contrast_label)
    self.contrast_sliders = []
    for n, band in enumerate(contrast_data):
      inner_layout = QHBoxLayout()
      inner_layout.setSpacing(5)
      slider = QSlider(Qt.Horizontal)
      slider.setMinimum(0)
      slider.setMaximum(127)
      slider.setValue(band["data"])
      self.contrast_sliders.append(slider)
      spin_box = QSpinBox()
      spin_box.setMinimum(0)
      spin_box.setMaximum(127)
      spin_box.setValue(band["data"])
      spin_box.valueChanged.connect(slider.setValue)
      spin_box.setStyleSheet(spinbox_stylesheet.format(color=band["color"]))
      slider.valueChanged.connect(spin_box.setValue)
      inner_layout.addWidget(spin_box)
      inner_layout.addWidget(slider)
      contrast_layout.addLayout(inner_layout)
    h_layout.addLayout(contrast_layout)

    layout.addLayout(h_layout)
    layout.addWidget(buttonBox)
    self.setLayout(layout)

  def accept_and_finish(self):
    for contrast in self.window.image_data.contrastIter():
      if contrast == 0:
        # Can't allow it, otherwise it would divide by zero (A = contrast' / contrast)
        QMessageBox.critical(self, "Operation failed", "The picture has a band with 0 contrast. The operation was halted.")
        self.reject()
        return
    self.signals.done.emit((
      tuple(map(lambda x: x.value(), self.brightness_sliders)),
      tuple(map(lambda x: x.value(), self.contrast_sliders))
    ))
    self.accept()