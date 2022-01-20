from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework.fields import Field
from rest_framework import permissions


# fmt: off
CREATE = 1 << 1  # 2
READ   = 1 << 2  # 4
UPDATE = 1 << 3  # 8
DELETE = 1 << 4  # 16

ALL = CREATE | READ | UPDATE | DELETE

PERMISSIONS = {
    "create": CREATE,
    "read"  : READ,
    "update": UPDATE,
    "delete": DELETE,
}

REQUEST_PERMISSIONS = {
    "GET"  : READ,
    "POST" : CREATE,
    "PUT"  : UPDATE,
    "PATCH": UPDATE,
    "DELETE": DELETE,
}


# fmt: on
def permission_is_valid(value) -> bool:
    value = int(value)

    valid_perm = any([not not (value & perm) for perm in PERMISSIONS.values()])
    is_even = value % 2 == 0

    # is the permission within the valid range, even number, and a valid permmision ?
    return value <= ALL and is_even and valid_perm


# Django class permissions
class ValidateProjectPermissions(permissions.BasePermission):
    message = "Not allowed to perform this action."

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj) -> bool:
        is_author = obj.author == request.user
        is_contributor = request.user in obj.contributors.all()

        # Author can perform any action on the project
        # Contributor can only perform read actions on the project

        if is_author:
            return True

        if is_contributor:
            return request.method in ["GET", "HEAD"]

        # has_permission = False
        # req_permission = REQUEST_PERMISSIONS[request.method]

        # if is_contributor:
        #     contributor_obj = obj.contributors.get(user=request.user)
        #     has_permission = contributor_obj.permission & req_permission

        # return is_author or has_permission


class ValidateContributorPermissions(permissions.BasePermission):
    pass


class ValidateIssuePermissions(permissions.BasePermission):
    pass


class ValidateCommentPermissions(permissions.BasePermission):
    pass


# serializer field
class PermissionField(Field):
    default_error_messages = {
        "invalid": _("This permission is invalid."),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if permission_is_valid(data):
            return int(data)
        else:
            self.fail("invalid")

    def to_representation(self, value):
        return int(value)


def validate_permissions(value: int) -> bool:
    if not isinstance(value, int):
        raise ValidationError(_("Permission must be an integer"))

    if not permission_is_valid(value):
        raise ValidationError(_("%(value)s is not a valid permission"), params={"value": value})
