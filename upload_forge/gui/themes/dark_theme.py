from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt

def apply_dark_theme(app):
    app.setStyle("Fusion")
    
    # Custom Font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Modern Dark Palette
    dark_bg = QColor(30, 30, 30)
    darker_bg = QColor(20, 20, 20)
    text_color = QColor(230, 230, 230)
    accent_color = QColor(0, 122, 204) # Visual Studio Blue-ish
    success_color = QColor(92, 184, 92)
    
    palette = QPalette()
    palette.setColor(QPalette.Window, dark_bg)
    palette.setColor(QPalette.WindowText, text_color)
    palette.setColor(QPalette.Base, darker_bg)
    palette.setColor(QPalette.AlternateBase, dark_bg)
    palette.setColor(QPalette.ToolTipBase, text_color)
    palette.setColor(QPalette.ToolTipText, dark_bg)
    palette.setColor(QPalette.Text, text_color)
    palette.setColor(QPalette.Button, dark_bg)
    palette.setColor(QPalette.ButtonText, text_color)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, accent_color)
    palette.setColor(QPalette.Highlight, accent_color)
    palette.setColor(QPalette.HighlightedText, Qt.white)
    
    app.setPalette(palette)
    
    # Additional StyleSheet for finer control
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e1e;
        }
        QTabWidget::pane {
            border: 1px solid #333;
            background: #1e1e1e;
        }
        QTabBar::tab {
            background: #2d2d2d;
            color: #bbb;
            padding: 10px 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background: #3e3e3e;
            color: white;
            border-bottom: 2px solid #007acc;
        }
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #252526;
            border: 1px solid #3e3e3e;
            color: #d4d4d4;
            padding: 5px;
            border-radius: 3px;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid #007acc;
        }
        QPushButton {
            background-color: #0e639c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #1177bb;
        }
        QPushButton:pressed {
            background-color: #094771;
        }
        QPushButton:disabled {
            background-color: #333;
            color: #888;
        }
        QTableWidget {
            gridline-color: #333;
            selection-background-color: #264f78;
        }
        QHeaderView::section {
            background-color: #252526;
            color: #d4d4d4;
            padding: 8px;
            border: none;
            border-bottom: 2px solid #007acc;
            font-weight: bold;
        }
        QProgressBar {
            border: none;
            border-radius: 5px;
            text-align: center;
            background: #252526;
            color: white;
            font-weight: bold;
        }
        QProgressBar::chunk {
            background-color: #007acc;
            border-radius: 5px;
        }
        QSplitter::handle {
            background-color: #333;
        }
        QScrollBar:vertical {
            border: none;
            background: #1e1e1e;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #424242;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QLabel {
            color: #d4d4d4;
        }
        /* About Section Styling */
        QLabel#aboutTitle {
            font-size: 28px;
            font-weight: bold;
            color: #007acc;
            margin-bottom: 10px;
        }
        QLabel#aboutDesc {
            font-size: 14px;
            color: #cccccc;
            line-height: 1.4;
        }
        QWidget#aboutContainer {
            background-color: #252526;
            border-radius: 10px;
            border: 1px solid #333;
        }
    """)
