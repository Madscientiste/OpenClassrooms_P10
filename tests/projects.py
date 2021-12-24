import requests
import json

from rich.console import Console

from . import __loader

from .__config import BASE_URL, DEFAULT_USER_PASSWORD, FAKE
from .__functions import get_user, save_json, authenticated_request


URL = BASE_URL + "/projects/"
PROJECT_TYPES = ["IOS", "ANDROID", "FRONT-END", "BACK-END"]
TEST_ORDER = 2

state = {}
console = Console()


@__loader.register_test(order=1)
def create_project(*args, **kwargs):
    """Attempt to create a project"""

    payload = {"title": FAKE.name(), "description": FAKE.text(), "type": FAKE.random_element(PROJECT_TYPES)}

    # Create a project
    user = get_user()
    req = authenticated_request(user, url=URL, data=payload, method="POST")
    project = json.loads(req.text)

    assert req.status_code == 201, "Failed to create project, didn't get 201"
    # log("[green]\[success][reset]: Created project", f"{project['title']}")

    state["created_project"] = project
    state["used_user"] = user


@__loader.register_test(order=2)
def get_project(*args, **kwargs):
    """Get the previous created project using an ID"""

    created_project = state["created_project"]
    user = state["used_user"]

    req = authenticated_request(user, url=URL + f"{created_project['id']}/", method="GET")
    project = json.loads(req.text)

    assert req.status_code == 200, "Failed to get project, didn't get 200"
    assert created_project == project, "Fetched project doesn't match created project"
    # log("[green]\[success][reset]: Got project", f"{project['title']}")

    state["got_project"] = project
    state["used_user"] = user


@__loader.register_test(order=3)
def edit_created_project(*args, **kwargs):
    """Attempt to edit the previously created project"""

    project = state["created_project"]
    user = state["used_user"]

    payload = {"title": FAKE.name(), "description": FAKE.text(), "type": FAKE.random_element(PROJECT_TYPES)}
    req = authenticated_request(user, url=URL + str(project["id"]) + "/", data=payload, method="PUT")
    project = json.loads(req.text)

    assert req.status_code == 200, "Failed to edit project, didn't get 200"
    # log("[green]\[success][reset]: Edited project with random data", f"{project['title']}")

    state["created_project"] = project
    state["used_user"] = user


@__loader.register_test(order=4)
def delete_created_project(*args, **kwargs):
    """Attempt to delete the previously created project"""

    project = state["created_project"]
    user = state["used_user"]

    req = authenticated_request(user, url=URL + str(project["id"]) + "/", method="DELETE")
    assert req.status_code == 204, "Failed to delete project, didn't get 204"
    # log("[green]\[success][reset]: Deleted project", f"{project['title']}")
