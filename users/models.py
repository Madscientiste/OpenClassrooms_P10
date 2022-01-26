from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Contributor(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    class Meta:
        unique_together = ("user", "project")


class User(AbstractUser):
    projects = models.ManyToManyField("projects.Project", through="Contributor")
