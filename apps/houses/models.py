from django.db import models


class House(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default="#ffffff")
    motto = models.CharField(max_length=255, blank=True, null=True)
    total_points = models.IntegerField(default=0)

    # 🧠 NUOVO: icona/logo
    icon = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to="house_logos/", blank=True, null=True)

    def __str__(self):
        return self.name