from functools import wraps
from project.utils.traces import push_span


def trace(name: str | None = None):
    """
    Create a span around a function.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            push_span(name or func.__name__)
            #try:
            return func(*args, **kwargs)

            #finally:
            #    print("DEBUG: Decorator Done!")

        return wrapper

    return decorator

