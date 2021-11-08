from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QMdiArea, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from rgb_effects.common.display_signals import DisplaySignals

class EqualizationDisplay(QDialog):
  def __init__(self, window, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.signals = DisplaySignals()
    self.windows = window.mdiArea().subWindowList(order=QMdiArea.ActivationHistoryOrder)[::-1]
    self.setWindowTitle("Equalization Operation")
    self.titles = list(map(lambda x: x.title, self.windows))
    qbtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(qbtn)
    buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept_and_finish)
    buttonBox.rejected.connect(self.reject)
    layout = QVBoxLayout()
    layout.setSpacing(10)

    layout.addWidget(QLabel("Picture to Equalize"))
    self.a_combobox = QComboBox()
    self.a_combobox.addItems(self.titles)
    layout.addWidget(self.a_combobox)

    layout.addWidget(buttonBox)
    self.setLayout(layout)

  def accept_and_finish(self):
    a = self.windows[self.a_combobox.currentIndex()]
    title = f"Equalization: {a.title}"
    self.signals.done.emit((a.image_data, {"title": title}))
    self.accept()