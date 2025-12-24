import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from pylunix import CheckBox

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setStyleSheet("background-color: #222222;")
    layout = QVBoxLayout(window)

    btn = CheckBox("Check Box")
    layout.addWidget(btn)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()