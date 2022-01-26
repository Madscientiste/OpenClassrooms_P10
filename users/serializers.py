from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from projects.serializers import ProjectSerializer
from projects.models import Project

from .models import User, Contributor


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=None)
    username = serializers.CharField(write_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), write_only=True, required=True)
    # permission = PermissionField()

    class Meta:
        model = Contributor
        fields = "__all__"

    def validate_user(self, attrs):
        username = self.initial_data["username"]

        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

    def create(self, validated_data):
        validated_data.pop("username")

        # can't add the author of a project as a contributor
        project = validated_data.get("project")

        if project.author == validated_data["user"]:
            raise serializers.ValidationError({"detail": "Can't add the author of a project as a contributor"})

        return super().create(validated_data)
