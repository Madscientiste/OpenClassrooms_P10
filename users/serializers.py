from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from SoftDesk_API.permissions import PermissionField
from projects.serializers import ProjectSerializer
from projects.models import Project

from .models import User, Contributor


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}


class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(write_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), write_only=True, required=True)
    permission = PermissionField(required=True)

    class Meta:
        model = Contributor
        fields = ("id", "user", "username", "project", "permission")

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(), fields=("user", "project"), message="Contributor already added"
            )
        ]

    def validate_user(self, attrs):
        data = super().is_valid(attrs)

        username = data.pop("username")
        data["user"] = User.objects.get(username=username)

        return data
    
    