import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from pylunix import PasswordBox

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setStyleSheet("background-color: #222222;")
    layout = QVBoxLayout(window)

    password_box = PasswordBox()
    layout.addWidget(password_box)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()