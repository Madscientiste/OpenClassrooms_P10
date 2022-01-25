from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "title", "description", "type", "author")
        read_only_fields = ["id", "author"]
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "type": {"required": False},
        }

    # author is only here to be able to create a project
    def create(self, validated_data):
        user = self.context["request"].user
        return Project.objects.create(author=user, **validated_data)
