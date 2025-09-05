import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.Login.login import LoginWidget
from services.auth_service import AuthService
from ui.Login.Dashboard import Dashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.login_widget = LoginWidget()
        
        self.setCentralWidget(self.login_widget)
        
        self.setWindowTitle("CISC Virtual Hub - Login")
        self.setGeometry(100, 100, 900, 600)
        
        self.login_widget.login_successful.connect(self.open_dashboard)

    def open_dashboard(self, result):
        print(f"Login OK for {result.username} | roles={result.roles} | primary={result.primary_role}")

        self.dashboard = Dashboard(
            username=result.username,
            roles=result.roles,
            primary_role=result.primary_role,
            token=result.token
        )
        self.dashboard.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
