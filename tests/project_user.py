import requests
import json

from rich.console import Console

from . import __loader

from .__config import BASE_URL, DEFAULT_USER_PASSWORD, FAKE
from .__functions import get_user, save_json, authenticated_request


URL = BASE_URL + "/projects/"
PROJECT_TYPES = ["IOS", "ANDROID", "FRONT-END", "BACK-END"]
TEST_ORDER = 3

state = {}
console = Console()
