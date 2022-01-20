from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from issues.models import Issue

from issues.serializers import IssueSerializer

from SoftDesk_API.permissions import ValidateIssuePermissions
from SoftDesk_API.tools import mutable_request


# /projects/<project_pk>/issues/
# /projects/<project_pk>/issues/<issue_pk>/
class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, ValidateIssuePermissions]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk", -1)
        issues = get_object_or_404(Issue, project_id=project_id)
        return issues

    @mutable_request
    def create(self, request, project_pk):
        request.data.update(project=project_pk, author=request.user.id)
        
        
        return super().create(request)
