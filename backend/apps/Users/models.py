from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

# create and adjust base user, merge auth_user -> Profile 
class BaseUser(AbstractUser):
    """Custom model that would inherit and extend the AbstractBaseUser"""
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    suffix = models.CharField(max_length=5, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    institutional_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

class FacultyDepartment(models.Model):
    department_name = models.CharField(max_length=50)

class Position(models.Model):
    position_id=models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=50)


class Program(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_name= models.CharField(max_length=255)

class Section(models.Model):
    section_id=models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=10)

class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", db_column="user_id")
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
    admin_id = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="admin", db_column="admin_id")

class Faculty(models.Model):
    faculty_id = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="faculty", db_column="faculty_id")
    faculty_department = models.ForeignKey(FacultyDepartment, on_delete=models.SET_NULL, null=True)
    # position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    hire_date = models.DateField(null=True, blank=True)


class Student(models.Model):
    student_id = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="student", db_column="student_id")
    program = models.ForeignKey("Program", on_delete=models.SET_NULL, null=True)
    indiv_points = models.IntegerField(default=0)
    year_level = models.IntegerField()


class Staff(models.Model):
    staff_id = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="staff", db_column="staff_id")
    faculty_department = models.ForeignKey(FacultyDepartment, on_delete=models.SET_NULL, null=True)
    job_title = models.CharField(max_length=50)
