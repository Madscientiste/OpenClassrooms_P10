# ------------------------
# # define intital setup for tests
# create users and aquire the tokens for later use.
from faker import Faker

from .__config import USERS_TO_CREATE
from .__functions import create_users, authenticate_users, load_json

# this is run before everything, because we need to create some users before
def __init__():
    try:
        load_json("users.json")
    except FileNotFoundError:
        create_users(USERS_TO_CREATE)
