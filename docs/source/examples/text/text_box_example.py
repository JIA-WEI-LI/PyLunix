import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from pylunix import TextBox

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setStyleSheet("background-color: #222222;")
    layout = QVBoxLayout(window)

    text_box = TextBox()
    layout.addWidget(text_box)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()