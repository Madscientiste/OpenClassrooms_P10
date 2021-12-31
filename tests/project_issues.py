import requests
import json

from rich.console import Console

from . import __loader

from .__config import BASE_URL, DEFAULT_USER_PASSWORD, FAKE, CONSOLE
from .__functions import get_user, save_json, authenticated_request


URL = BASE_URL + "/projects/{0}/issues/"

ISSUE_PRIORITY = ["LOW", "MEDIUM", "HIGH"]
ISSUE_TAG = ["BUG", "IMPROVEMENT", "TASK"]
ISSUE_STATUS = ["TODO", "IN PROGRESS", "DONE"]

TEST_ORDER = 3

state = {}


@__loader.register_test(order=1, fixture="project_fixture")
def create_project_issue(project, user):
    """Attempt to create an issue for a project."""

    payload = {
        "title": FAKE.name(),
        "desc": FAKE.text(),
        "tag": FAKE.random_element(ISSUE_TAG),
        "priority": FAKE.random_element(ISSUE_PRIORITY),
        "status": FAKE.random_element(ISSUE_STATUS),
    }

    req = authenticated_request(user, url=URL.format(project["id"]), data=payload, method="POST")
    issue = json.loads(req.text)

    assert req.status_code == 201, f"Failed to create an issue, didn't get 201, got {req.status_code} instead"


@__loader.register_test(order=2, fixture="project_fixture")
def edit_created_issue(project, user):
    """Attempt to edit the previously created issue."""

    payload = {
        "title": FAKE.name(),
        "desc": FAKE.text(),
        "tag": FAKE.random_element(ISSUE_TAG),
        "priority": FAKE.random_element(ISSUE_PRIORITY),
        "status": FAKE.random_element(ISSUE_STATUS),
    }

    url = URL.format(project["id"]) + f"{state['created_issue']['id']}/"
    req = authenticated_request(user, url=url, data=payload, method="PUT")
    issue = json.loads(req.text)

    assert req.status_code == 201, f"Failed to edit an issue, didn't get 201, got {req.status_code} instead"

    state["edited_issue"] = issue
    state["used_user"] = user

    return state
