from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = [
        ("CEO", 'CEO'),
        ("PM", "PM"),
        ("Consultant", "Consultant"),
        ("Tl", "Team Leader"),
        ("Planner", "Planner"),
    ]

    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=GENDERS)
    role = models.CharField(max_length=50, choices=ROLES)

    def __str__(self):
        return f"{self.username} ({self.role})"