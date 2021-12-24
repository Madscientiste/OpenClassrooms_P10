from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import Field

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

# fmt: on
class Permissions:
    def __init__(self, value: int):
        self.value = int(value)

    def __repr__(self):
        return f"Permissions({self.value})"

    def has_permission(self, name: str) -> bool:
        permission = PERMISSIONS[name]
        return self.value & permission == permission

    @property
    def is_valid(self) -> bool:
        valid_perm = any([not not (self.value & perm) for perm in PERMISSIONS.values()])
        is_even = self.value % 2 == 0

        # is the value within the valid range, even and a valid permmision ?
        return self.value <= ALL and is_even and valid_perm


# serializer field
class PermissionField(Field):
    default_error_messages = {
        "invalid": _("This permission is invalid."),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if Permissions(data).is_valid:
            return int(data)
        else:
            self.fail("invalid")

    def to_representation(self, value):
        return int(value)


def validate_permissions(value: int) -> bool:
    if not isinstance(value, int):
        raise ValidationError(_("Permission must be an integer"))

    if not Permissions(value).is_valid:
        raise ValidationError(_("%(value)s is not a valid permission"), params={"value": value})
