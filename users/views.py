from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions

from .models import Contributor
from projects.models import Project

from .serializers import ContributorSerializer

from SoftDesk_API.permissions import ValidateContributorPermissions
from SoftDesk_API.tools import mutable_request

# /projects/<project_pk>/contributors/
# /projects/<project_pk>/contributors/<contributor_pk>/
class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, ValidateContributorPermissions]

    def get_queryset(self):
        project_pk = self.kwargs.get("project_pk")

        if not project_pk.isdigit():
            raise ValidationError({"detail": "Invalid project_pk"})

        project = Project.objects.get(pk=project_pk)
        return Contributor.objects.filter(project=project)

    @mutable_request
    def create(self, request, project_pk):
        request.data.update(project=project_pk)
        return super().create(request)
