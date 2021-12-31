import requests
import json

from .__config import BASE_URL, JSON_OUTPUT, DEFAULT_USER_PASSWORD, FAKE, CONSOLE
from . import __loader

# --------------------------------------------------
#


def save_json(data, filename):
    with open(JSON_OUTPUT / filename, "w") as f:
        json.dump(data, f)


def load_json(filename):
    with open(JSON_OUTPUT / filename, "r") as f:
        return json.load(f)


def fail(*args, **kwargs):
    """Print a fail message and exit with code 1"""
    CONSOLE.log("[red]\[failed][/red]", *args, **kwargs)
    exit(1)


# --------------------------------------------------
# these are for the "initial" setup, however, they can be used in cli


@__loader.register_function("create_users")
def create_users(*args, **kwargs):
    """Create users and save them to a json file"""
    amount = int(args[0]) if args else None

    if not amount:
        fail("not enough arguments")

    print(f"Creating {amount} users...")

    url = BASE_URL + "/signup/"
    users = []

    for i in range(amount):
        user = gen_random_user()
        user["password2"] = DEFAULT_USER_PASSWORD

        req = requests.post(url, data=user)
        response = json.loads(req.text)
        users.append(response)

        if req.status_code != 201:
            fail(f"Failed to create user [{user['username']}], didn't get 201")

        print(f"Created user [{user['username']}] ({i + 1}/{amount})")

    save_json(users, "users.json")


@__loader.register_function("login_users")
def authenticate_users():
    """Authenticate created users, update the json file when done"""
    print("Authenticating users...")

    url = BASE_URL + "/login/"
    users = load_json("users.json")

    for idx, user in enumerate(users):
        pyaload = {"username": user["username"], "password": DEFAULT_USER_PASSWORD}

        req = requests.post(url, data=pyaload)
        response = json.loads(req.text)

        users[idx]["auth"] = {
            "refresh": response["refresh"],
            "access": response["access"],
        }

        if req.status_code != 200:
            fail(f"Failed to authenticate user [{user['username']}], didn't get 200")

        print(f"Authenticated user [{user['username']}] ({idx + 1}/{len(users)})")

    save_json(users, "users.json")


# --------------------------------------------------
# these are utility functions for the "tests", keeping it very minimal is very important.


def gen_random_user() -> dict:
    """Generate a random user using faker, return a dict"""
    return {
        "username": FAKE.user_name(),
        "password": DEFAULT_USER_PASSWORD,
        "email": FAKE.email(),
        "first_name": FAKE.first_name(),
        "last_name": FAKE.last_name(),
    }


def get_user(random_pick: bool = False, rules: dict = None):
    """Get the first user from the json file, if random_pick is True, return a random user
    if rules is not None, return a user that matches the rules
    """

    users = load_json("users.json")
    return users[FAKE.random_int(0, len(users) - 1)] if random_pick else users[0]


def authenticated_request(user: dict, *args, **kwargs):
    """Send a request to the server, with the user's token"""
    recursing = kwargs.pop("recursing", False)

    if "auth" not in user:
        user = aquire_user_token(user)

    headers = {"Authorization": f"Bearer {user['auth']['access']}"}
    req = requests.request(*args, **kwargs, headers=headers)

    if req.status_code == 401 and not recursing:
        user = refresh_user(user)
        return authenticated_request(user, recursing=True, *args, **kwargs)

    return req


def aquire_user_token(user: dict):
    """Aquire a user's token, update the json file, return the new user ( basically a login )"""

    url = BASE_URL + "/login/"
    pyaload = {"username": user["username"], "password": DEFAULT_USER_PASSWORD}

    req = requests.post(url, data=pyaload)
    response = json.loads(req.text)

    users = load_json("users.json")

    idx = users.index(user)

    if req.status_code == 200:
        users[idx]["auth"] = {
            "refresh": response["refresh"],
            "access": response["access"],
        }

        save_json(users, "users.json")

        return users[idx]
    else:
        fail("Failed to aquire user token", response)


def refresh_user(user: dict):
    """Refresh a user's token, return the new refresh token"""

    url = BASE_URL + "/login/refresh/"
    pyaload = {"refresh": user["auth"]["refresh"]}

    req = requests.post(url, data=pyaload)
    response = json.loads(req.text)

    if req.status_code == 200:
        user["auth"]["access"] = response["access"]
        return user
    else:
        fail("Failed to refresh user token", response)
