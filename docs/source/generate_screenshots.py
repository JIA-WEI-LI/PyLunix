import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from scripts.screenshots.gallery_showcase import *

output_path = os.path.join(os.path.dirname(__file__), "_static")
os.makedirs(output_path, exist_ok=True)

def capture_widget_image(app, widget_class, components_type:str, filename:str):
    window = widget_class()
    window.setWindowFlags(Qt.Widget)
    window.show()
    app.processEvents()
    pixmap = QPixmap(window.size())
    window.render(pixmap)
    img_path = os.path.join(output_path, components_type, filename)
    pixmap.save(img_path)
    window.close()
    print(f"✅ {filename} saved at: {img_path}")

if __name__ == "__main__":
    app = QApplication([])
    capture_widget_image(app, ScreenshotPushButton, "basic_inputs", "PushButton.png")
    capture_widget_image(app, ScreenshotPrimaryButton, "basic_inputs", "PrimaryButton.png")
    capture_widget_image(app, ScreenshotSubtleButton, "basic_inputs", "SubtleButton.png")
    capture_widget_image(app, ScreenshotHyperlinkButton, "basic_inputs", "HyperlinkButton.png")
    capture_widget_image(app, ScreenshotToggleButton, "basic_inputs", "ToggleButton.png")
    capture_widget_image(app, ScreenshotSubtleToggleButton, "basic_inputs", "SubtleToggleButton.png")