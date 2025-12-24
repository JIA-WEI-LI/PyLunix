import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from pylunix import ListBox

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setStyleSheet("background-color: #222222;")
    layout = QVBoxLayout(window)

    list_box = ListBox()
    list_box.addItems(["Item 1", "Item 2", "Item 3"])
    layout.addWidget(list_box)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()