from django.db.models import base
from rest_framework_nested import routers
from django.urls import include, path

from . import views

router = routers.DefaultRouter()
router.register(r"projects", views.ProjectViewSet, basename="projects")
# /projects/
# /projects/{project_id}/

user_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
user_router.register(r"users", views.ContributorViewSet, basename="users")
# /projects/{project_id}/users/
# /projects/{project_id}/users/{user_id}/

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(user_router.urls)),
]
