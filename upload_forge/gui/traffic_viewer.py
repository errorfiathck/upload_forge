from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                               QTableWidgetItem, QSplitter, QTextEdit, QLabel, QHeaderView)
from PySide6.QtCore import Qt
from ..core.vulnerability_models import TrafficLog

class TrafficViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.logs = []

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Splitter for List (Left) and Details (Right)
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: Traffic List
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Method", "URL", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemClicked.connect(self.display_details)
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.addWidget(QLabel("Request History"))
        left_layout.addWidget(self.table)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Right: Request/Response Details
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Request Box
        right_layout.addWidget(QLabel("Request"))
        self.req_text = QTextEdit()
        self.req_text.setReadOnly(True)
        right_layout.addWidget(self.req_text)
        
        # Response Box
        right_layout.addWidget(QLabel("Response"))
        self.res_text = QTextEdit()
        self.res_text.setReadOnly(True)
        right_layout.addWidget(self.res_text)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)

    def clear_logs(self):
        self.logs = []
        self.table.setRowCount(0)
        self.req_text.clear()
        self.res_text.clear()

    def add_log(self, log: TrafficLog):
        self.logs.append(log)
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # ID
        self.table.setItem(row, 0, QTableWidgetItem(str(log.id)))
        # Method
        self.table.setItem(row, 1, QTableWidgetItem(log.method))
        # URL
        self.table.setItem(row, 2, QTableWidgetItem(log.url))
        # Status
        status_item = QTableWidgetItem(str(log.status_code))
        
        # Color code status
        if 200 <= log.status_code < 300:
            status_item.setForeground(Qt.green)
        elif 400 <= log.status_code < 500:
            status_item.setForeground(Qt.yellow)
        elif 500 <= log.status_code:
            status_item.setForeground(Qt.red)
            
        self.table.setItem(row, 3, status_item)

    def display_details(self, item):
        row = item.row()
        if row < len(self.logs):
            log = self.logs[row]
            
            # Format Request
            req_str = f"{log.method} {log.url}\n\n[Headers]\n{log.request_headers}\n\n[Body]\n{log.request_body}"
            self.req_text.setText(req_str)
            
            # Format Response
            res_str = f"Status: {log.status_code}\n\n[Headers]\n{log.response_headers}\n\n[Body]\n{log.response_body}"
            self.res_text.setText(res_str)
