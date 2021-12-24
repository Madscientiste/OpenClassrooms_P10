#
#
#
#

tests = []


def register_test(order: int = 1):
    """Test registration decorator

    - file order: this is the highest level, for example: a user need to be tested before creating a project for him,
        its set using a variable called`TEST_ORDER`

    - function order: this is the lowest level, for example: you might need to create a project then check if it has been created,
        then add a user to it, then check if the user has been added to the project ect ect, its set using the `order` parameter


    the tests are loaded with the variable, and the function are called with order params.
    """

    def decorator(function):
        priotiy = function.__globals__.get("TEST_ORDER", 0)
        tests.append((priotiy, order, function))
        return function

    return decorator
