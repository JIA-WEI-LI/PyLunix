import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from pylunix import ToggleButton

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setStyleSheet("background-color: #222222;")
    layout = QVBoxLayout(window)

    btn = ToggleButton("Toggle Button")
    layout.addWidget(btn)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()