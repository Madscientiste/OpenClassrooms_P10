from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from issues.models import Issue

from issues.serializers import IssueSerializer

from SoftDesk_API.permissions import ValidateIssuePermissions
from SoftDesk_API.tools import mutable_request
from projects.models import Project


# /projects/<project_pk>/issues/
# /projects/<project_pk>/issues/<issue_pk>/
class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, ValidateIssuePermissions]

    def get_queryset(self):
        project_pk = self.kwargs.get("project_pk", -1)

        if not project_pk.isdigit():
            raise ValidationError({"detail": "Invalid project_pk"})

        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            raise ValidationError({"detail": "Project does not exist"})

        try:
            return Issue.objects.filter(project=project)
        except Issue.DoesNotExist:
            raise ValidationError({"detail": "Issue does not exist"})

    @mutable_request
    def create(self, request, project_pk):
        request.data.update(project=project_pk, author=request.user.id)
        return super().create(request)

    @mutable_request
    def update(self, request, project_pk, *args, **kwargs):
        request.data.update(project=project_pk, author=request.user.id)
        return super().update(request, *args, **kwargs)
