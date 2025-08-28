import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from PyQt6.QtWidgets import QApplication
from backend.db import init_pool
from backend.apps.Users.db_script import UserRepository
from backend.apps.Users.service import AuthService
from frontend.ui.login.login import LoginWidget

def build_dependencies():
    init_pool()
    repo = UserRepository()
    auth = AuthService(repo)
    return auth

def run():
    app = QApplication(sys.argv)
    auth = build_dependencies()
    win = LoginWidget(auth_service=auth)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()
