#
#
#


# For some reason this works on my env (Windows), but not on Linux.
def mutable_request(func):
    """Make the request.data mutable"""

    def wrapper(*args, **kwargs):
        args[1].data._mutable = True
        return func(*args, **kwargs)

    return wrapper
