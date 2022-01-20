import requests
import json

from rich.console import Console

from SoftDesk_API.permissions import PERMISSIONS
from . import __loader

from .__config import BASE_URL, DEFAULT_USER_PASSWORD, FAKE, CONSOLE
from .__functions import get_user, save_json, authenticated_request, load_json


URL = BASE_URL + "/projects/{0}/users/"

TEST_ORDER = 3

state = {}


@__loader.register_test(order=1, fixture="project_fixture")
def project_user(project, user):
    """Attempt to add, get and delete a user from a project"""
    # you shouldn't add the creator of the project as a contributor
    users = [u["username"] for u in load_json("users.json") if u["username"] != user["username"]]

    payload = {
        "username": FAKE.random_element(users),
        "permission": 30,
        "role": FAKE.word(),
    }

    req = authenticated_request(user, url=URL.format(project["id"]), data=payload, method="POST")
    user = json.loads(req.text)

    # check if user has the same value of the payload
    assert req.status_code == 201, f"Status code: {req.status_code}"
    assert user.get("id") is not None, "user has no ID"

    # check if the added user is in the project
    req = authenticated_request(user, url=URL.format(project["id"]), method="GET")
    users = json.loads(req.text)

    assert req.status_code == 200, f"Status code: {req.status_code}"
    assert payload["username"] in [u["username"] for u in users], "user didn't get added"

    # delete the user
    req = authenticated_request(user, url=URL.format(project["id"]) + str(user["id"]), method="DELETE")
    assert req.status_code == 204, f"Status code: {req.status_code}"

    # check if the user is deleted
    req = authenticated_request(user, url=URL.format(project["id"]), method="GET")
    users = json.loads(req.text)

    assert req.status_code == 200, f"Status code: {req.status_code}"
    assert payload["username"] not in [u["username"] for u in users], "user didn't get deleted"
