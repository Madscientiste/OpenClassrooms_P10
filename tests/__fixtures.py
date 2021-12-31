import json


from . import __loader
from .__functions import authenticated_request, get_user, save_json, load_json
from .__config import BASE_URL, FAKE


@__loader.register_fixure("project_fixture")
def project_fixture() -> dict:
    """Create a project, and return it"""

    from .projects import PROJECT_TYPES

    project = {
        "title": FAKE.name(),
        "description": FAKE.text(),
        "type": FAKE.random_element(PROJECT_TYPES),
    }

    user = get_user()

    url = BASE_URL + "/projects/"
    project_req = authenticated_request(user, url=url, data=project, method="POST")
    project_json = json.loads(project_req.text)
    project.update(project_json)

    assert project_req.status_code == 201
    assert project.get("id") is not None

    return {"project": project, "user": user}


@__loader.register_fixure("issue_fixture")
def issue_fixture() -> dict:
    """Create an issue, and return it"""

    from .projects import PROJECT_TYPES
    from .project_issues import ISSUE_PRIORITY, ISSUE_TAG, ISSUE_STATUS

    project = {
        "title": FAKE.name(),
        "description": FAKE.text(),
        "type": FAKE.random_element(PROJECT_TYPES),
    }

    issue = {
        "title": FAKE.name(),
        "desc": FAKE.text(),
        "tag": FAKE.random_element(ISSUE_TAG),
        "priority": FAKE.random_element(ISSUE_PRIORITY),
        "status": FAKE.random_element(ISSUE_STATUS),
    }

    user = get_user()

    url = BASE_URL + "/projects/"
    project_req = authenticated_request(user, url=url, data=project, method="POST")
    project_json = json.loads(project_req.text)
    project.update(project_json)

    assert project_req.status_code == 201
    assert project.get("id") is not None

    url = BASE_URL + f"/projects/{project['id']}/issues/"
    issue_req = authenticated_request(user, url=url, data=issue, method="POST")
    issue_json = json.loads(issue_req.text)
    issue.update(issue_json)

    assert issue_req.status_code == 201
    assert issue.get("id") is not None

    project["issue"] = issue
