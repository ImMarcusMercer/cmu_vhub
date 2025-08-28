# from django.db import models

# # Create your models here.

# # User model based on the DB structure
# # class User(models.Model):
# #     """Should contain all necessary fields to accomodate User functionality"""
# #     user_id=models.IntegerField()
# #     role_id=models.IntegerField()
# #     first_name=models.CharField(max_length=50)
# #     middle_name=models.CharField(max_length=50)
# #     last_name=models.CharField(max_length=50)
# #     hash_password=models.CharField(max_length=255)
# #     email=models.CharField(max_length=50)

# #     # Need confirmation on what to use, for now use (supabase/image/UID/profile_image). Not real, sample only
# #     profile_picture=models.CharField(max_length=50)

# #     status=models.PositiveSmallIntegerField()
# #     creation_date=models.DateTimeField()
# #     birth_date=models.DateTimeField()
# #     institutional_id=models.IntegerField()
# #     phone_number=models.IntegerField()
# #     program=models.CharField(max_length=50)
# #     section_id=models.IntegerField()
# #     is_staff=models.BooleanField()
# #     is_active=models.BooleanField()
# #     is_superuser=models.BooleanField()
# #     last_login=models.DateTimeField()
# #     date_joined=models.DateTimeField()

# # users/models.py
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils import timezone

# class User(AbstractUser):
#     # Replaces Django’s default AutoField PK with your explicit user_id if needed
#     # user_id = models.AutoField(primary_key=True)

#     # Additional fields from your DBD
#     middle_name = models.CharField(max_length=50, blank=True)
#     profile_picture = models.URLField(blank=True)  # Supabase/public link
#     status = models.PositiveSmallIntegerField(default=1)  # map to enum
#     creation_date = models.DateTimeField(auto_now_add=True)
#     birth_date = models.DateField(null=True, blank=True)
#     institutional_id = models.CharField(max_length=50, blank=True, unique=True)
#     phone_number = models.CharField(max_length=20, blank=True)
#     program = models.CharField(max_length=50, blank=True)

#     # Foreign keys from other tables (Roles, section)
#     section = models.ForeignKey("Section", on_delete=models.SET_NULL, null=True, blank=True)
#     role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True, blank=True)

#     # Already provided by AbstractUser:
#     # first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}".strip()

# class Role(models.Model):
#     role_name = models.CharField(max_length=50, unique=True)
#     access_level = models.PositiveSmallIntegerField()

#     def __str__(self):
#         return self.role_name

# class Section(models.Model):
#     section_name = models.CharField(max_length=10)

#     def __str__(self):
#         return self.section_name

# class Resume(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     filepath = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.user.username} resume"

from dataclasses import dataclass
from typing import Sequence

@dataclass
class UserRow:
    id: int
    username: str
    password_hash: str
    status: str

@dataclass
class AuthResult:
    ok: bool
    error: str | None = None
    user_id: int | None = None
    username: str | None = None
    roles: Sequence[str] = ()
    token: str | None = None 
