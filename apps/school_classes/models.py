from django.db import models


class SchoolClass(models.Model):
    name = models.CharField(max_length=50)  # es: 5A INF
    year = models.IntegerField()
    section = models.CharField(max_length=5)

    def __str__(self):
        return self.name