from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QColor

class ResultsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["Risk", "Vulnerability", "Payload", "Confidence", "Details"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)

    def clear_results(self):
        self.setRowCount(0)

    def add_finding(self, finding):
        row = self.rowCount()
        self.insertRow(row)
        
        risk_item = QTableWidgetItem(finding.risk_level)
        if finding.risk_level == "Critical":
            risk_item.setForeground(QColor("red"))
        elif finding.risk_level == "High":
            risk_item.setForeground(QColor("orange"))
        
        self.setItem(row, 0, risk_item)
        self.setItem(row, 1, QTableWidgetItem(finding.name))
        self.setItem(row, 2, QTableWidgetItem(finding.payload))
        self.setItem(row, 3, QTableWidgetItem(finding.confidence))
        self.setItem(row, 4, QTableWidgetItem(finding.proof[:50] + "..."))
