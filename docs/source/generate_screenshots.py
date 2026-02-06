import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint

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

def capture_flyout_image(app, widget_class, components_type:str, filename:str):
    window = widget_class()
    window.show()

    if hasattr(window, 'prepare_for_screenshot'):
        window.prepare_for_screenshot()
    
    app.processEvents()
    import time
    time.sleep(0.3)

    main_rect = window.geometry() 
    fly_rect = window.flyout.geometry()
    
    main_pixmap = window.grab()
    fly_pixmap = window.flyout.grab()
    combined_rect = main_rect.united(fly_rect)

    padding = 20
    final_pixmap = QPixmap(combined_rect.width() + padding*2, combined_rect.height() + padding*2)
    final_pixmap.fill(Qt.transparent)

    painter = QPainter(final_pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)

    main_draw_pos = main_rect.topLeft() - combined_rect.topLeft() + QPoint(padding, padding)
    fly_draw_pos = fly_rect.topLeft() - combined_rect.topLeft() + QPoint(padding, padding)

    painter.drawPixmap(main_draw_pos, main_pixmap)
    painter.drawPixmap(fly_draw_pos, fly_pixmap)
    painter.end()
    
    img_path = os.path.join(output_path, components_type, filename)
    final_pixmap.save(img_path, "PNG")
    
    window.flyout.close()
    window.close()
    print(f"✅ Clean screenshot saved: {img_path}")

if __name__ == "__main__":
    app = QApplication([])
    capture_widget_image(app, ScreenshotPushButton, "basic_inputs", "PushButton.png")
    capture_widget_image(app, ScreenshotPrimaryButton, "basic_inputs", "PrimaryButton.png")
    capture_widget_image(app, ScreenshotSubtleButton, "basic_inputs", "SubtleButton.png")
    capture_widget_image(app, ScreenshotHyperlinkButton, "basic_inputs", "HyperlinkButton.png")
    capture_widget_image(app, ScreenshotToggleButton, "basic_inputs", "ToggleButton.png")
    capture_widget_image(app, ScreenshotSubtleToggleButton, "basic_inputs", "SubtleToggleButton.png")
    capture_widget_image(app, ScreenshotRepeatButton, "basic_inputs", "RepeatButton.png")
    capture_widget_image(app, ScreenshotRichTextBlock, "text", "RichTextBlock.png")
    capture_widget_image(app, ScreenshotTextBlock, "text", "TextBlock.png")
    capture_widget_image(app, ScreenshotToolButton, "basic_inputs", "ToolButton.png")
    capture_widget_image(app, ScreenshotPrimaryToolButton, "basic_inputs", "PrimaryToolButton.png")
    capture_widget_image(app, ScreenshotSubtleToolButton, "basic_inputs", "SubtleToolButton.png")
    capture_widget_image(app, ScreenshotToggleToolButton, "basic_inputs", "ToggleToolButton.png")
    capture_widget_image(app, ScreenshotSubtleToggleToolButton, "basic_inputs", "SubtleToggleToolButton.png")
    capture_widget_image(app, ScreenshotTextBox, "text", "TextBox.png")
    capture_flyout_image(app, ScreenshotFlyout, "dialogs_and_flyouts", "Flyout.png")