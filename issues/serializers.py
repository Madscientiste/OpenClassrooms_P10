from rest_framework import serializers

from .models import Issue

# created_time, is read only
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ["created_time"]
