import requests
import json

from rich.console import Console

from SoftDesk_API.permissions import PERMISSIONS
from . import __loader

from .__config import BASE_URL, DEFAULT_USER_PASSWORD, FAKE, CONSOLE
from .__functions import get_user, save_json, authenticated_request


URL = BASE_URL + "/projects/users/"
TEST_ORDER = 3

state = {}

# user:3
# permission:30
# role:afaefaefaefaef


# @__loader.register_test(order=1)
# def create_project(*args, **kwargs):
#     """Attempt to create a project"""

#     payload = {
#         "user": 0,
#         "permission": 0,
#         "role": 0,
#     }
