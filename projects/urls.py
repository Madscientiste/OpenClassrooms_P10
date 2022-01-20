from django.db.models import base
from rest_framework_nested import routers
from django.urls import include, path

from .views import ProjectViewSet
from users.views import ContributorViewSet
from issues.views import IssueViewSet
from comments.views import CommentViewSet

router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="projects")
# /projects/
# /projects/{project_id}/

user_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
user_router.register(r"users", ContributorViewSet, basename="users")
# /projects/{project_id}/users/
# /projects/{project_id}/users/{user_id}/

issue_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
issue_router.register(r"issues", IssueViewSet, basename="issues")
# /projects/{project_id}/issues/
# /projects/{project_id}/issues/{issue_id}/

issue_comment_router = routers.NestedSimpleRouter(issue_router, r"issues", lookup="issue")
issue_comment_router.register(r"comments", CommentViewSet, basename="comments")
# /projects/{project_id}/issues/{issue_id}/comments/
# /projects/{project_id}/issues/{issue_id}/comments/{comment_id}/

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(user_router.urls)),
    path(r"", include(issue_router.urls)),
    path(r"", include(issue_comment_router.urls)),
]
