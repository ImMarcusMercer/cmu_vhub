from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self, username: str, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Dashboard")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        welcome = QLabel(f"Welcome to the Dashboard, {username}!", self)
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("font-size: 20px; font-weight: bold;")

        layout.addWidget(welcome)
