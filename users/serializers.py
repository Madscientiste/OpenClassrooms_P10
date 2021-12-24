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


class ContributorSerializer(NestedHyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), write_only=True)
    permission = PermissionField(required=True)

    class Meta:
        model = Contributor
        fields = ("user", "project", "permission", "role")

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(), fields=("user", "project"), message="Contributor already added"
            )
        ]
