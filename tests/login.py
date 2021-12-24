import requests
import json

from . import __loader

from .__config import BASE_URL, DEFAULT_USER_PASSWORD
from .__functions import get_user

url = BASE_URL + "/login/"

TEST_ORDER = 1


@__loader.register_test()
def login_should_success(*args, **kwargs):
    """Attempt to login a valid user"""

    user = get_user(random_pick=True)
    user["password"] = DEFAULT_USER_PASSWORD

    req = requests.post(url, data=user)

    assert req.status_code == 200, "Login should be successful, didn't get 200"


@__loader.register_test()
def login_should_fail(*args, **kwargs):
    """Attempt to login an invalid user"""

    user = get_user(random_pick=True)
    user["password"] = "wrong password"

    req = requests.post(url, data=user)

    assert req.status_code == 401, "Login should have failed, didn't get 401"
