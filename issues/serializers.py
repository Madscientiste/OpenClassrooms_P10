from rest_framework import serializers

from projects.models import Project
from .models import Issue, issue_priority, issue_tag, issue_status

# created_time, is read only
class IssueSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), write_only=True, required=True)

    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ["created_time"]
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "tag": {"required": False},
            "priority": {"required": False},
            "status": {"required": False},
        }
