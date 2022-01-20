from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from issues.models import Issue
from comments.serializers import CommentSerializer

from SoftDesk_API.permissions import ValidateCommentPermissions
from SoftDesk_API.tools import mutable_request


# /projects/<project_pk>/issues/<issue_pk>/comments/
# /projects/<project_pk>/issues/<issue_pk>/comments/<comment_pk>/
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, ValidateCommentPermissions]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk", -1)
        issue_id = self.kwargs.get("issue_pk", -1)

        comments = get_object_or_404(Issue, project_id=project_id, pk=issue_id)
        return comments.all()

    @mutable_request
    def create(self, request, project_pk, issue_pk):
        request.data.update(project=project_pk, issue=issue_pk, author=request.user.id)
        return super().create(request)
