# PyLunix

[![Version](https://img.shields.io/badge/version-0.2.0--alpha.2-yellow)](#)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](#)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.11-blue)](#)

> [!WARNING]
> This project is still under development and is not yet complete

## Project Overview

**PyLunix** is a custom user interface (UI) widget library developed using **PyQt5**. The project aims to emulate and implement the design language and interface style of Microsoft **WinUI 3**, offering a set of modern, aesthetic, and visually consistent UI components—such as PushButtons—for Python desktop applications.

PyLunix is designed to provide developers with a lightweight and easily integrated solution to enhance the user experience and visual quality of their PyQt5 applications.

## Key Features

* **WinUI 3 Design Adoption:** The core design strictly adheres to the visual specifications of WinUI 3 (Windows App SDK), providing a familiar, modern interface aesthetic.
* **PyQt5 Implementation:** Built upon the powerful, cross-platform capabilities of PyQt5, ensuring stable operation of widgets across various operating systems.
* **Core Component Set (`v0.2.0-alpha.2`):** The library now provides a foundational set of **ten core interactive widgets** including `Buttons`, `Check Boxes`, `Toggle Buttons` ... , ready for immediate use.
* **Simple API Access:** All components are easily accessible through a direct import from the top-level package (`from pylunix import *`), simplifying integration.
* **Custom and Extensible:** All components are custom-implemented, allowing developers deep customization and extension to meet specific application requirements.
---

## Installation and Quick Start

### Installation
Currently, the project is not distributed via PyPI. You must clone the repository and install dependencies manually.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/JIA-WEI-LI/PyLunix.git](https://github.com/JIA-WEI-LI/PyLunix.git)
    cd PyLunix
    ```
2.  **Install dependencies:**
    ```bash
    # Assuming you are using pip and a virtual environment
    pip install PyQt5
    ```

### Usage Example
You can now import the core widgets directly:

```python
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from pylunix import PushButton # or just use *

if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)
    
    # Example of using a newly available widget
    my_button = PushButton("Click Me")
    layout.addWidget(my_button)
    
    window.setWindowTitle("PyLunix Demo")
    window.show()
    app.exec_()
```

## Component Status & Roadmap

This section tracks the implementation progress of core UI components based on the WinUI 3 design specification.

### Implemented Widgets ( `0.2.0-alpha.2` Focus )
> [!NOTE]
> No selection box indicates that the API is not publicly available.
* **Basic Inputs**
    * `BaseButton`
      * [x] `PushButton` ( *WinUI3 Base* )
      * [x] `PrimaryButton` 
      * [x] `TransparentPushButton`
    * [x] `HyperlinkButton` ( *WinUI3 Base* )
    * [x] `RepeatButton` ( *WinUI3 Base* )
    * [x] `ToggleButton` ( *WinUI3 Base* )
      * [x] `TransparentToggleButton`
      * [x] `SegmentedButton`
    * [x] `ToolButton`
      * [x] `TransparentToolButton`
    * [x] `CheckBox` ( *WinUI3 Base* )
    * [x] `RadioButton` ( *WinUI3 Base* )
* **Collections**
    * [x] `ListBox` ( *WinUI3 Base* )
* **Text**
    * `_BaseTextBoxEdit`
      * `TextBoxEdit`
      * [x] `TextBox` ( *WinUI3 Base* )
      * `PasswordBoxEdit`
      * [x] `PasswordBox` ( *WinUI3 Base* )
      * `NumberBoxEdit`
      * [x] `NumberBox` ( *WinUI3 Base* )
    * [x] `RichTextBlock` ( *WinUI3 Base* )
    * [x] `TextBlock` ( *WinUI3 Base* )

## Contributing
We welcome contributions from anyone interested in modern UI design and PyQt5 development. If you wish to contribute, please:

1. Fork the repository.

2. Create your feature branch (`git checkout -b feature/AmazingFeature`).

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).

4. Push to the branch (`git push origin feature/AmazingFeature`).

5. Open a Pull Request.

## License
This project is licensed under the [LICENSE](LICENSE). See the LICENSE file for details

## Contact
    
Project Maintainer: [Magicsoldier19 - HomePage](https://github.com/JIA-WEI-LI)

Project Link: [PyLunix - GitHub](https://github.com/JIA-WEI-LI/PyLunix)