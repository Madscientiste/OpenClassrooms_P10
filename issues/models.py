from django.db import models
from django.conf import settings

issue_priority = [
    ("LOW", "low"),
    ("MEDIUM", "medium"),
    ("HIGH", "high"),
]

issue_tag = [
    ("BUG", "bug"),
    ("IMPROVEMENT ", "improvement"),
    ("TASK", "task"),
]

issue_status = [
    ("TODO", "todo"),
    ("IN PROGRESS", "in progress"),
    ("DONE", "done"),
]


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=2024)
    tag = models.CharField(max_length=128, choices=issue_tag)
    priority = models.CharField(max_length=128, choices=issue_priority)
    status = models.CharField(max_length=128, choices=issue_status)
    created_time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    assignee_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignee_user")
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)