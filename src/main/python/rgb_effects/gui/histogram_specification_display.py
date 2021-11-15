from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QMdiArea, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from rgb_effects.common.display_signals import DisplaySignals

class HistogramSpecificationDisplay(QDialog):
  def __init__(self, window, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.signals = DisplaySignals()
    self.windows = window.mdiArea().subWindowList(order=QMdiArea.ActivationHistoryOrder)[::-1]
    self.setWindowTitle("Histogram Specification Operation")
    self.titles = list(map(lambda x: x.title, self.windows))
    qbtn = QDialogButtonBox.Apply | QDialogButtonBox.Cancel
    buttonBox = QDialogButtonBox(qbtn)
    buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept_and_finish)
    buttonBox.rejected.connect(self.reject)
    layout = QVBoxLayout()
    layout.setSpacing(10)

    layout.addWidget(QLabel("Target image"))
    self.a_combobox = QComboBox()
    self.a_combobox.addItems(self.titles)
    layout.addWidget(self.a_combobox)
    layout.addWidget(QLabel("Reference histogram image"))
    self.b_combobox = QComboBox()
    self.b_combobox.addItems(self.titles)
    if len(self.titles) > 1:
      self.b_combobox.setCurrentIndex(1)
    layout.addWidget(self.b_combobox)

    layout.addWidget(buttonBox)
    self.setLayout(layout)

  def accept_and_finish(self):
    a = self.windows[self.a_combobox.currentIndex()]
    b = self.windows[self.b_combobox.currentIndex()]
    title = f"Histogram Specification: {a.title} - {b.title}"
    self.signals.done.emit((a.image_data, b.image_data, {"title": title}))
    self.accept()