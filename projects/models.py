from django.db import models
from django.conf import settings

project_choices = [
    ("BACK-END", "back-end"),
    ("FRONT-END", "front-end"),
    ("IOS", "IOS"),
    ("ANDROID", "Android"),
]


class Project(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(max_length=128, choices=project_choices)
    contributors = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="contributors", through="users.Contributor")
