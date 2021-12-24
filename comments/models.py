from django.db import models
from django.conf import settings


class Comment(models.Model):
    description = models.CharField(max_length=2024)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey("issues.Issue", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
