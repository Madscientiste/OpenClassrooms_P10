from pathlib import Path
from faker import Faker

#
#
#
#
#

BASE_URL = "http://localhost:8000"

JSON_OUTPUT = Path(__file__).parent / "data"
JSON_OUTPUT.mkdir(exist_ok=True)

USERS_TO_CREATE = 10
DEFAULT_USER_PASSWORD = "123456789A!"

FAKE = Faker()
