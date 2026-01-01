import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QTabWidget, QFormLayout, QTextEdit, QProgressBar, QMessageBox,
                               QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
from .themes.dark_theme import apply_dark_theme
from .scanner_worker import ScannerWorker
from .results_table import ResultsTable
from .traffic_viewer import TrafficViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UploadForge - Professional Vulnerability Scanner")
        self.resize(1100, 750)
        
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Header
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #252526; border-bottom: 1px solid #333;")
        header_layout = QHBoxLayout(header_widget)
        
        self.header_label = QLabel("🛡️ UPLOAD FORGE")
        self.header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #007acc; padding: 10px;")
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        
        self.main_layout.addWidget(header_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Init Tabs
        self.init_config_tab()
        self.init_results_tab()
        self.init_traffic_tab()
        self.init_logs_tab()
        self.init_about_tab()
        
        # Status Bar
        self.statusBar().setStyleSheet("background-color: #007acc; color: white; font-weight: bold;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.statusBar().showMessage("Ready")

        self.worker = None

    def init_config_tab(self):
        self.config_tab = QWidget()
        main_layout = QHBoxLayout()
        
        # Left side: Form
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("http://example.com/upload.php")
        form_layout.addRow("Target URL:", self.url_input)
        
        self.param_input = QLineEdit("file")
        form_layout.addRow("File Parameter:", self.param_input)
        
        self.upload_dir_input = QLineEdit()
        self.upload_dir_input.setPlaceholderText("http://example.com/uploads/")
        form_layout.addRow("Upload Directory (Optional):", self.upload_dir_input)
        
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("http://127.0.0.1:8080")
        form_layout.addRow("Proxy:", self.proxy_input)
        
        self.headers_input = QLineEdit()
        self.headers_input.setPlaceholderText("Authorization: Bearer Token")
        form_layout.addRow("Headers:", self.headers_input)
        
        self.scan_btn = QPushButton("🚀 Start Scan")
        self.scan_btn.setCursor(Qt.PointingHandCursor)
        self.scan_btn.setFixedHeight(45)
        self.scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                font-size: 14px; 
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.scan_btn.clicked.connect(self.start_scan)
        
        form_widget.setLayout(form_layout)
        
        # Right side: Info/Graphic
        info_widget = QWidget()
        info_layout = QVBoxLayout()
        info_label = QLabel("Scanner Configuration")
        info_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #007acc;")
        info_desc = QLabel("Configure the target parameters carefully.\nEnsure you have permission to test the target.")
        info_desc.setStyleSheet("color: #888; font-style: italic;")
        
        info_layout.addWidget(info_label)
        info_layout.addWidget(info_desc)
        info_layout.addStretch()
        info_layout.addWidget(self.scan_btn)
        info_widget.setLayout(info_layout)
        
        main_layout.addWidget(form_widget, stretch=2)
        main_layout.addWidget(info_widget, stretch=1)
        
        self.config_tab.setLayout(main_layout)
        self.tabs.addTab(self.config_tab, "Configuration")

    def init_results_tab(self):
        self.results_tab = QWidget()
        layout = QVBoxLayout()
        self.results_table = ResultsTable()
        layout.addWidget(self.results_table)
        self.results_tab.setLayout(layout)
        self.tabs.addTab(self.results_tab, "Results")

    def init_traffic_tab(self):
        self.traffic_viewer = TrafficViewer()
        self.tabs.addTab(self.traffic_viewer, "Traffic Viewer")

    def init_logs_tab(self):
        self.logs_tab = QWidget()
        layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("font-family: Consolas, monospace; font-size: 12px;")
        layout.addWidget(self.log_output)
        self.logs_tab.setLayout(layout)
        self.tabs.addTab(self.logs_tab, "Logs")

    def init_about_tab(self):
        self.about_tab = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        container = QWidget()
        container.setObjectName("aboutContainer")
        container.setFixedWidth(600)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("Upload Forge")
        title.setObjectName("aboutTitle")
        title.setAlignment(Qt.AlignCenter)
        
        desc = QLabel(
            "Version 1.0.0\n\n"
            "Upload Forge is a professional-grade security tool designed for "
            "detecting and exploiting file upload vulnerabilities.\n\n"
            "Features:\n"
            "• Async Scanning Engine\n"
            "• Advanced Payload Generation\n"
            "• Real-time Traffic Analysis\n"
            "• Detailed Reporting\n\n"
            "Created by ErrorFiat"
        )
        desc.setObjectName("aboutDesc")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        
        container_layout.addWidget(title)
        container_layout.addWidget(desc)
        
        layout.addWidget(container)
        self.about_tab.setLayout(layout)
        self.tabs.addTab(self.about_tab, "About")

    def log(self, message):
        self.log_output.append(message)

    def start_scan(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "URL is required")
            return
            
        param = self.param_input.text().strip()
        upload_dir = self.upload_dir_input.text().strip() or None
        proxies = self.proxy_input.text().strip() or None
        headers_str = self.headers_input.text().strip()
        
        headers = {}
        if headers_str:
            try:
                # Simple parsing for "Key: Value"
                key, value = headers_str.split(":", 1)
                headers[key.strip()] = value.strip()
            except:
                self.log("Invalid headers format. Use 'Key: Value'")

        proxy_dict = {"http://": proxies, "https://": proxies} if proxies else None

        self.scan_btn.setEnabled(False)
        self.scan_btn.setText("Scanning...")
        self.results_table.clear_results()
        self.log_output.clear()
        
        # Clear previous traffic logs
        self.traffic_viewer.clear_logs()

        self.worker = ScannerWorker(url, param, upload_dir, proxy_dict, headers)
        self.worker.progress.connect(self.log)
        self.worker.finding_found.connect(self.results_table.add_finding)
        self.worker.traffic_log.connect(self.traffic_viewer.add_log) # Connect traffic signal
        self.worker.finished.connect(self.scan_finished)
        self.worker.start()

    def scan_finished(self, result):
        self.scan_btn.setEnabled(True)
        self.scan_btn.setText("🚀 Start Scan")
        self.log(f"Scan finished. Found {len(result.findings)} vulnerabilities.")
        self.statusBar().showMessage("Scan Completed")
        QMessageBox.information(self, "Scan Complete", f"Scan finished.\nFound {len(result.findings)} vulnerabilities.")

def run_gui():
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
