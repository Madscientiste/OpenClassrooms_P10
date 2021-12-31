from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import Model
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.http import Http404

from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Project
from users.models import Contributor, User
from issues.models import Issue

from .serializers import ProjectSerializer
from users.serializers import ContributorSerializer, UserSerializer
from issues.serializers import IssueSerializer
from comments.serializers import CommentSerializer

def mutable_request(func):
    """Make the request.data mutable"""

    def wrapper(*args, **kwargs):
        args[1].data._mutable = True
        return func(*args, **kwargs)

    return wrapper


# /projects/
# /projects/{project_id}/
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)

    @mutable_request
    def create(self, request):
        request.data.update(author=request.user.id)
        return super().create(request)

    @mutable_request
    def update(self, request, *args, **kwargs):
        request.data.update(author=request.user.id)
        return super().update(request, *args, **kwargs)


# /projects/<project_pk>/contributors/
# /projects/<project_pk>/contributors/<contributor_pk>/
class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk", -1)
        project = get_object_or_404(Project, pk=project_id)
        return project.contributors.all()

    @mutable_request
    def create(self, request, project_pk):
        request.data.update(project=project_pk)
        return super().create(request)

    def destroy(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs.get("project_pk", -1)

            contributor = Contributor.objects.get(user=kwargs.get("pk"), project=project_id)
            contributor.delete()
            return Response(status=204)

        except Contributor.DoesNotExist:
            return Response({"error": "Contributor not found"}, status=404)


# /projects/<project_pk>/issues/
# /projects/<project_pk>/issues/<issue_pk>/
class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk", -1)
        issues = get_object_or_404(Issue, project_id=project_id)
        return issues.all()

    @mutable_request
    def create(self, request, project_pk):
        request.data.update(project=project_pk, author=request.user.id)
        return super().create(request)


# /projects/<project_pk>/issues/<issue_pk>/comments/
# /projects/<project_pk>/issues/<issue_pk>/comments/<comment_pk>/
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk", -1)
        issue_id = self.kwargs.get("issue_pk", -1)

        comments = get_object_or_404(Issue, project_id=project_id, pk=issue_id)
        return comments.all()

    @mutable_request
    def create(self, request, project_pk, issue_pk):
        request.data.update(project=project_pk, issue=issue_pk, author=request.user.id)
        return super().create(request)
