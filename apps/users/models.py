from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Studente'),
        ('teacher', 'Docente'),
        ('teamleader', 'Team Leader'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    school_class = models.ForeignKey(
        'school_classes.SchoolClass',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    house = models.ForeignKey(
        'houses.House',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    questionnaire_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def is_teacher(self):
        return self.role in ('teacher', 'admin')

    @property
    def is_student(self):
        return self.role == 'student'
