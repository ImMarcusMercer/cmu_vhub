from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FacultyDepartment(models.Model):
    department_name = models.CharField(max_length=50)


class Position(models.Model):
    position_name = models.CharField(max_length=50)


class Program(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_name= models.CharField(max_length=255)

class Section(models.Model):
    section_name = models.CharField(max_length=10)

class Profile(models.Model):
    # profile_id = models.AutoField(primary_key=True)
    # user_id = models.ForeignKey(User.pk)
    # middle_name = models.CharField(max_length=20)
    # suffix = models.CharField(auto_created=None)
    # profile_picture = models.CharField()
    # birth_date = models.DateField()
    # institutional_id = models.CharField(max_length=20)
    # phone_number = models.CharField(max_length=11)
    # role_type = None
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    suffix = models.CharField(max_length=5, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    institutional_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("student", "Student"),
        ("faculty", "Faculty"),
        ("staff", "Staff"),
    ]
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Admin(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="admin")

class Faculty(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="faculty")
    faculty_department = models.ForeignKey(FacultyDepartment, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    hire_date = models.DateField(null=True, blank=True)


class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="student")
    program = models.ForeignKey("Program", on_delete=models.SET_NULL, null=True)
    indiv_points = models.IntegerField(default=0)
    year_level = models.IntegerField()


class Staff(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="staff")
    faculty_department = models.ForeignKey(FacultyDepartment, on_delete=models.SET_NULL, null=True)
    job_title = models.CharField(max_length=50)


