import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from pylunix import Flyout, PushButton, TextBlock

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setStyleSheet("background-color: #222222;")
    layout = QVBoxLayout(window)

    flyout = Flyout()
    btn = PushButton("Empty cart")
    # Flyout Content
    flyout_layout = QVBoxLayout()
    flyout_layout.addWidget(TextBlock("All items will be removed. Do you want to continue?"))
    close_btn = PushButton("Yes, empty my cart")
    close_btn.clicked.connect(flyout.close)
    flyout_layout.addWidget(close_btn)
    # Set Flyout Content
    flyout.set_content_layout(flyout_layout)
    # Show Flyout on Button Click
    btn.clicked.connect(lambda: flyout.show_at(btn))
    layout.addWidget(btn)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
