from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from rest_framework.fields import Field
from rest_framework import permissions

from users.models import User, Contributor
from projects.models import Project
from issues.models import Issue
from comments.models import Comment


class defaultPermissionMessage:
    message = "You don't have permission to perform this action."

    def can_read(self, request, view):
        """Check if the user has access to the object

        Only a Contributor or a Project owner can read the object and its underlying.
        """
        allowed_methods = ["GET", "POST"]
        project = self.get_project(view.kwargs["project_pk"])

        is_project_author = project.author == request.user
        is_contributor = request.user in project.contributors.all()

        return is_project_author or is_contributor

    def can_write(self, request, obj):
        """Check if the user is an author of an object

        Only the author of an object can update it or delete it.

        -> GET request returns True by default
        """
        if request.method in ["PUT", "DELETE"]:
            return obj.author == request.user
        elif request.method == "GET":
            return True
        else:
            return False

    def get_project(self, project_pk) -> Project:
        try:
            return Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            raise ValidationError({"detail": "Project does not exist"})

    def get_contributor(self, user_pk) -> Contributor:
        try:
            return Contributor.objects.get(pk=user_pk)
        except Contributor.DoesNotExist:
            raise ValidationError({"detail": "Contributor does not exist"})

    def get_issue(self, issue_pk) -> Issue:
        try:
            return Issue.objects.get(pk=issue_pk)
        except Issue.DoesNotExist:
            raise ValidationError({"detail": "Issue does not exist"})

    def get_comment(self, comment_pk) -> Comment:
        try:
            return Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise ValidationError({"detail": "Comment does not exist"})


# Django class permissions
class ValidateProjectPermissions(permissions.BasePermission, defaultPermissionMessage):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj) -> bool:
        is_author = obj.author == request.user
        is_contributor = request.user in obj.contributors.all()
        return is_author or (is_contributor and request.method == "GET")


class ValidateContributorPermissions(permissions.BasePermission, defaultPermissionMessage):
    # Author can perform any action on the project
    # Contributor can only perform read actions on the project if he is a contributor
    def has_permission(self, request, view):
        return self.can_read(request, view)

    def has_object_permission(self, request, view, obj) -> bool:
        return self.can_write(request, obj)


class ValidateIssuePermissions(permissions.BasePermission, defaultPermissionMessage):
    def has_permission(self, request, view):
        return self.can_read(request, view)

    def has_object_permission(self, request, view, obj) -> bool:
        return self.can_write(request, obj)


class ValidateCommentPermissions(permissions.BasePermission, defaultPermissionMessage):
    def has_permission(self, request, view):
        return self.can_read(request, view)

    def has_object_permission(self, request, view, obj):
        return self.can_write(request, obj)
