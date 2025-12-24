import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from pylunix import NumberBox

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setStyleSheet("background-color: #222222;")
    layout = QVBoxLayout(window)

    number_box = NumberBox()
    number_box.setAcceptsExpression(True)
    layout.addWidget(number_box)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()