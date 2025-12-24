import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from pylunix import TextBlock 

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("TextBlock Example")
    window.resize(400, 300)
    window.setStyleSheet("background-color: #222222;")
    
    layout = QVBoxLayout(window)
    text_block = TextBlock()
    
    example_content = "This is a TextBlock example."
    text_block.setText(example_content)
    layout.addWidget(text_block)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()