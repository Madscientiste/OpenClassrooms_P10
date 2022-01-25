from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

from issues.models import Issue
from comments.serializers import CommentSerializer

from SoftDesk_API.permissions import ValidateCommentPermissions
from SoftDesk_API.tools import mutable_request

from projects.models import Project
from .models import Comment

# /projects/<project_pk>/issues/<issue_pk>/comments/
# /projects/<project_pk>/issues/<issue_pk>/comments/<comment_pk>/
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_pk = self.kwargs.get("project_pk", -1)
        issue_pk = self.kwargs.get("issue_pk", -1)

        if not project_pk.isdigit():
            raise ValidationError({"detail": "Invalid project_id"})

        if not issue_pk.isdigit():
            raise ValidationError({"detail": "Invalid issue_id"})

        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            raise ValidationError({"detail": "Project does not exist"})

        try:
            issue = Issue.objects.get(pk=issue_pk, project=project)
        except Issue.DoesNotExist:
            raise ValidationError({"detail": "Issue does not exist"})

        return Comment.objects.filter(issue=issue)
        # return Issue.objects.get(pk=issue_pk, project=project)

    @mutable_request
    def create(self, request, project_pk, issue_pk):
        request.data.update(project=project_pk, issue=issue_pk, author=request.user.id)
        return super().create(request)
