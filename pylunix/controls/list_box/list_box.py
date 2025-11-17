from PyQt5.QtWidgets import QWidget, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from ...common.stylesheet import PyLunixStyleSheet

class ListBox(QListWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setProperty("class", "ListBox")
        self.setMinimumHeight(200)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        PyLunixStyleSheet.LIST_BOX.apply(self)