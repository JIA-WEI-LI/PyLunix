import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from pylunix import RichTextBlock

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setStyleSheet("background-color: #222222;")
    layout = QVBoxLayout(window)

    text_block = RichTextBlock("RichTextBlock Example: <b>This is bold text</b>, "
    "<i>this is italic</i>, and <span style='color: #FF5733;'>this is colored text</span>. "
    "You can also include <a href='https://www.google.com/?hl=zh_TW'>links</a>. ")
    layout.addWidget(text_block)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
