from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.base import Model

from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from .models import Project
from issues.models import Issue

from .serializers import ProjectSerializer
from issues.serializers import IssueSerializer
from comments.serializers import CommentSerializer

from SoftDesk_API.permissions import ValidateProjectPermissions, ValidateIssuePermissions, ValidateCommentPermissions
from SoftDesk_API.tools import mutable_request

# /projects/
# /projects/{project_id}/
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, ValidateProjectPermissions]

    def get_queryset(self):
        user_id = self.request.user.id
        return Project.objects.filter(Q(contributors__id=user_id) | Q(author=user_id))

    @mutable_request
    def create(self, request):
        request.data.update(author=request.user.id)
        return super().create(request)

    @mutable_request
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
