from django.shortcuts import render

# Create your views here.
import bcrypt
from uuid import uuid4
from datetime import datetime, timedelta, timezone

from django.db import connection, transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginSerializer

class LoginView(APIView):
    """
    POST /api/login/
    { "username": "...", "password": "..." }

    200 OK:
    {
      "ok": true,
      "user": {"id": 1, "username": "dummy_user", "status": "active"},
      "roles": ["Admin", "Staff"],
      "token": "3b7c6bdc-...."           # from auth_sessions
    }

    400/401:
    { "ok": false, "error": "Invalid username or password." }
    """

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        username = ser.validated_data["username"]
        password = ser.validated_data["password"]

        # 1) Lookup user
        with connection.cursor() as cur:
            cur.execute("""
                SELECT id, username, password_hash, status
                FROM users
                WHERE username = %s
            """, [username])
            row = cur.fetchone()

        if not row:
            # intentionally vague to avoid user enumeration
            return Response({"ok": False, "error": "Invalid username or password."},
                            status=status.HTTP_401_UNAUTHORIZED)

        user_id, username_db, password_hash, status_text = row

        if status_text != "active":
            return Response({"ok": False, "error": "Account is not active."},
                            status=status.HTTP_403_FORBIDDEN)

        # 2) Verify bcrypt
        try:
            ok = bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except Exception:
            return Response({"ok": False, "error": "Password check failed."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not ok:
            # optional: bump failed attempts
            with connection.cursor() as cur, transaction.atomic():
                cur.execute("""
                    UPDATE users SET failed_attempts = failed_attempts + 1 WHERE id = %s
                """, [user_id])
            return Response({"ok": False, "error": "Invalid username or password."},
                            status=status.HTTP_401_UNAUTHORIZED)

        # 3) Fetch roles
        with connection.cursor() as cur:
            cur.execute("""
                SELECT r.name
                FROM roles r
                JOIN user_roles ur ON ur.role_id = r.id
                WHERE ur.user_id = %s
            """, [user_id])
            roles = [r[0] for r in cur.fetchall()]

        # 4) Create session token (8h)
        token = str(uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(hours=8)
        with connection.cursor() as cur, transaction.atomic():
            cur.execute("""
                INSERT INTO auth_sessions(token, user_id, expires_at)
                VALUES (%s, %s, %s)
            """, [token, user_id, expires_at])

        return Response({
            "ok": True,
            "user": {"id": user_id, "username": username_db, "status": status_text},
            "roles": roles,
            "token": token,
        }, status=status.HTTP_200_OK)
