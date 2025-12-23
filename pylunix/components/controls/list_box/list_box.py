from PyQt5.QtWidgets import QWidget, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from ....common.stylesheet import PyLunixStyleSheet

class ListBox(QListWidget):
    """
    Themed selection list widget for displaying a collection of items.

    This class extends QListWidget to provide a clean, modern list interface 
    integrated with the PyLunix styling system. By default, it hides scrollbars 
    to maintain a minimalist aesthetic, making it suitable for fixed-size 
    menus or custom-scrolled containers.

    Attributes:
        None (Inherits all attributes from QListWidget).
    """
    def __init__(self, parent: QWidget = None):
        """
        Initialize the ListBox.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)

        self.setProperty("class", "ListBox")
        self.setMinimumHeight(200)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        PyLunixStyleSheet.LIST_BOX.apply(self)