# # backend/User/repository.py
# from typing import Optional, Sequence
# from backend.db import get_conn, put_conn
# from backend.apps.Users.models import UserRow
# import uuid
# from datetime import timedelta, datetime, timezone

# class UserRepository:
#     def get_by_username(self, username: str) -> Optional[UserRow]:
#         conn = get_conn()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                     SELECT id, username, password_hash, status
#                     FROM users
#                     WHERE username = %s
#                 """, (username,))
#                 row = cur.fetchone()
#                 if not row:
#                     return None
#                 return UserRow(id=row[0], username=row[1], password_hash=row[2], status=row[3])
#         finally:
#             put_conn(conn)

#     def get_roles(self, user_id: int) -> Sequence[str]:
#         conn = get_conn()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                     SELECT r.name
#                     FROM roles r
#                     JOIN user_roles ur ON ur.role_id = r.id
#                     WHERE ur.user_id = %s
#                 """, (user_id,))
#                 return [r[0] for r in cur.fetchall()]
#         finally:
#             put_conn(conn)

#     def bump_login_attempts(self, user_id: int):
#         conn = get_conn()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                     UPDATE users
#                     SET failed_attempts = failed_attempts + 1
#                     WHERE id = %s
#                 """, (user_id,))
#             conn.commit()
#         finally:
#             put_conn(conn)

#     def create_session(self, user_id: int, hours: int = 8) -> str:
#         conn = get_conn()
#         try:
#             token = str(uuid.uuid4())
#             exp = datetime.now(timezone.utc) + timedelta(hours=hours)
#             with conn.cursor() as cur:
#                 cur.execute("""
#                     INSERT INTO auth_sessions(token, user_id, expires_at)
#                     VALUES (%s, %s, %s)
#                 """, (token, user_id, exp))
#             conn.commit()
#             return token
#         finally:
#             put_conn(conn)

# backend/User/repository.py
from typing import Optional, Sequence
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.http import HttpRequest

User = get_user_model()  # This respects AUTH_USER_MODEL

class UserRepository:
    def get_by_username(self, username: str) -> Optional[AbstractBaseUser]:
        """Fetch a user by username using Django ORM"""
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get_roles(self, user_id: int) -> Sequence[str]:
        """Fetch user groups (roles)"""
        try:
            user = User.objects.get(pk=user_id)
            return list(user.groups.values_list("name", flat=True))
        except User.DoesNotExist:
            return []

    def bump_login_attempts(self, user_id: int):
        """Track failed login attempts (if you want a custom field)"""
        try:
            user = User.objects.get(pk=user_id)
            # If you’ve added a custom field failed_attempts in your custom User model:
            user.failed_attempts = (user.failed_attempts or 0) + 1
            user.save(update_fields=["failed_attempts"])
        except User.DoesNotExist:
            pass

    def create_session(self, request: HttpRequest, username: str, password: str) -> Optional[AbstractBaseUser]:
        """
        Authenticate and log in a user using Django's session framework.
        Returns the authenticated user, or None if authentication fails.
        """
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return user
        return None
