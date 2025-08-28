from backend.apps.Users.db_script import UserRepository
from backend.apps.Users.models import AuthResult
import bcrypt

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def login(self, username: str, password: str) -> AuthResult:
        """Used to validate user credentials
        reurn: user id, username, role(for permissions) and token (for session, cache or whatever you call it)"""
        user = self.repo.get_by_username(username)
        if not user:
            return AuthResult(ok=False, error="Invalid username or password.")

        if user.status != "active":
            return AuthResult(ok=False, error="Account is not active.")

        try:
            ok = bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8"))
        except Exception:
            return AuthResult(ok=False, error="Password check failed.")
        if not ok:
            self.repo.bump_login_attempts(user.id)
            return AuthResult(ok=False, error="Invalid username or password.")

        roles = self.repo.get_roles(user.id)
        token = self.repo.create_session(user.id)
        return AuthResult(ok=True, user_id=user.id, username=user.username, roles=roles, token=token)
