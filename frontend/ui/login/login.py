"""
PyQt6 Login UI (Wide Rectangular Card with Logo + Header Text)
"""

import sys
import re
import requests
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QLineEdit,
    QPushButton,
    QFrame,
    QGraphicsDropShadowEffect,
    QMessageBox
)

START_WIDTH = 1200
START_HEIGHT = 1080
MIN_WIDTH = 800
MIN_HEIGHT = 800


class LoginWidget(QWidget):
    forgot_password_requested = pyqtSignal()
    login_successful = pyqtSignal(str)  # Signal for successful login with email

    def __init__(self):
        super().__init__()

        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor("#f8f9fa"))
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        # Main layout split (left/right)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(40)

        # --- Left column ---
        left_layout = QVBoxLayout()
        left_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.left_logo = QLabel()
        self.left_logo.setPixmap(QPixmap("images/cisc.png").scaled(220, 220,Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.left_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.left_logo)

        self.left_label = QLabel("CISC VIRTUAL HUB")
        self.left_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        self.left_label.setStyleSheet("color: #6c757d;")
        self.left_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.left_label)

        left_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addLayout(left_layout, stretch=1)

        # --- Right column ---
        right_layout = QVBoxLayout()
        right_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Card frame (wide rectangle)
        card = QFrame()
        card.setFixedWidth(500)  # Set a fixed width for the card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 40))
        card.setGraphicsEffect(shadow)
        card.setStyleSheet("QFrame { background: white; border-radius: 8px; border: none; }")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)  # wide padding
        card_layout.setSpacing(16)

        # --- Top header with logo + university text ---
        header_layout = QHBoxLayout()

        # Logo placeholder
        self.uni_logo = QLabel()
        self.uni_logo.setPixmap(QPixmap("images/cmu.png").scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                                                          Qt.TransformationMode.SmoothTransformation))
        self.uni_logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(self.uni_logo)

        # University text
        text_layout = QVBoxLayout()
        self.uni_title = QLabel("Central Mindanao University")
        self.uni_title.setStyleSheet("color: #212529;")
        self.uni_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))

        self.uni_subtitle = QLabel("College of Information Sciences and Computing")
        self.uni_subtitle.setStyleSheet("color: #495057;")
        self.uni_subtitle.setFont(QFont("Segoe UI", 12))

        text_layout.addWidget(self.uni_title)
        text_layout.addWidget(self.uni_subtitle)
        header_layout.addLayout(text_layout)

        card_layout.addLayout(header_layout)

        # --- Divider ---
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #006400;")
        card_layout.addWidget(divider)

        # --- Sign In Form ---
        self.card_title = QLabel("Sign In")
        self.card_title.setStyleSheet("color: #212529; margin-top: 5px;")
        self.card_title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        card_layout.addWidget(self.card_title)

        # Email
        self.email_label = QLabel("Email")
        self.email_label.setStyleSheet("color: #495057; margin-top: 5px;")
        card_layout.addWidget(self.email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email")
        self.email_input.setStyleSheet("border: 1px solid #ccc; border-radius: 6px; padding: 10px;")
        card_layout.addWidget(self.email_input)

        self.email_error_label = QLabel()
        self.email_error_label.setStyleSheet("color: red; margin-left: 5px;")
        card_layout.addWidget(self.email_error_label)
        self.email_error_label.hide()

        # Password
        self.password_label = QLabel("Password")
        self.password_label.setStyleSheet("color: #495057; margin-top: 5px;")
        card_layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("border: 1px solid #ccc; border-radius: 6px; padding: 10px;")
        card_layout.addWidget(self.password_input)

        self.password_error_label = QLabel()
        self.password_error_label.setStyleSheet("color: red; margin-left: 5px;")
        card_layout.addWidget(self.password_error_label)
        self.password_error_label.hide()

        # Forgot Password
        self.forgot_password_link = QLabel("Forgot Password?")
        self.forgot_password_link.setStyleSheet(
            "QLabel { color: #007bff; } QLabel:hover { text-decoration: underline; }"
        )
        self.forgot_password_link.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.forgot_password_link.setCursor(Qt.CursorShape.PointingHandCursor)
        self.forgot_password_link.mousePressEvent = self.open_reset_password_window
        card_layout.addWidget(self.forgot_password_link)

        # Sign In button
        self.sign_in_btn = QPushButton("Sign In")
        self.sign_in_btn.setStyleSheet(
            "QPushButton { background-color: #006400; color: white; padding: 10px; "
            "border-radius: 6px; border: none; font-weight: bold; } "
            "QPushButton:hover { background-color: #228B22; }"
        )
        self.sign_in_btn.setMinimumHeight(38)
        self.sign_in_btn.clicked.connect(self.validate_login)
        card_layout.addWidget(self.sign_in_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add card to right column
        right_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        right_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addLayout(right_layout, stretch=3)  # wider card

        self.setLayout(main_layout)

        

    def open_reset_password_window(self, event):
        self.forgot_password_requested.emit()


    def validate_login(self):
        # Reset errors
        self.email_error_label.hide()
        self.password_error_label.hide()

        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        # Simple checks (same as before)...
        if not email or not password:
            self.password_error_label.setText("Both fields are required.")
            self.password_error_label.show()
            return

        try:
            url = "http://127.0.0.1:8000/api/login/"
            response = requests.post(url, data={"email": email, "password": password})

            if response.status_code == 200:
                self.login_successful.emit(email) 
            else:
                self.password_error_label.setText("Incorrect email or password.")
                self.password_error_label.show()

        except requests.exceptions.ConnectionError:
            self.password_error_label.setText("Cannot connect to server.")
            self.password_error_label.show()


    
