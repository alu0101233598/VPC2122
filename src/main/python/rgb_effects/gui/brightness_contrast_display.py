from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGridLayout
from PyQt5.QtCore import pyqtSignal

from rgb_effects.common.display_signals import DisplaySignals

class BrightnessContrastDisplay(QDialog):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Dialog initialization
    self.signals = DisplaySignals()
    qbtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(qbtn)
    buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept_and_finish)
    buttonBox.rejected.connect(self.reject)
    self.layout = QGridLayout()
    self.layout.addWidget(buttonBox)

    # Widget initialization
    self.setLayout(self.layout)

  def accept_and_finish(self):
    self.signals.done.emit((1, 2))
    self.accept()