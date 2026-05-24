from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.houses.models import House
from apps.school_classes.models import SchoolClass


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('leader', 'Team Leader'),
        ('teacher', 'Teacher'),
        ('superadmin', 'Super Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    school_email = models.EmailField(unique=True)

    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # 🔥 NUOVI CAMPI CORE
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True)

    onboarding_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username