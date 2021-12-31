#
#
#
#

tests = []
functions = []
fixtures = []


def register_test(order: int = 1, fixture: str = None):
    """Test registration decorator

    - file order: this is the highest level, for example: a user need to be tested before creating a project for him,
        its set using a variable called`TEST_ORDER`

    - function order: this is the lowest level, for example: you might need to create a project then check if it has been created,
        then add a user to it, then check if the user has been added to the project ect ect, its set using the `order` parameter


    the tests are loaded with the variable, and the function are called with order params.
    """

    def decorator(function):
        priotiy = function.__globals__.get("TEST_ORDER", 0)
        tests.append({"t_order": priotiy, "f_order": order, "function": function, "fixture": fixture})
        return function

    return decorator


def register_function(name: str = None, desc: str = None):
    """Register a function so they can be called using CLI"""

    def decorator(function):
        functions.append({"name": name or function.__name__, "desc": desc or function.__doc__, "function": function})
        return function

    return decorator


def register_fixture(name: str = None):
    """Register a fixture, so we can use it in a test"""

    def decorator(function):
        fixtures.append({"name": name or function.__name__, "function": function})
        return function

    return decorator
