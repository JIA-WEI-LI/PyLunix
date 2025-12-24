import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from pylunix import RichTextBlock 

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("RichTextBlock Example")
    window.resize(400, 300)
    window.setStyleSheet("background-color: #222222;")
    
    layout = QVBoxLayout(window)
    rich_text = RichTextBlock()
    
    example_content = """
    <h1>Welcome to PyLunix</h1>
    <p style='color: #ffffff;'>
        This is a <b>RichTextBlock</b> example. 
        It allows you to display formatted text easily within your UI.
    </p>
    <ul style='color: #aaaaaa;'>
        <li>Feature A: High Performance</li>
        <li>Feature B: Custom Styling</li>
    </ul>
    """
    rich_text.setText(example_content)
    layout.addWidget(rich_text)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()