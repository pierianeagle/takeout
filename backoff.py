import time

def retry(f, retries=5, backoff=1):
    """Exponential backoff decorator.

    Retries requests that raise an exception with exponential backoff.

    Args:
        retries: Maximum no. of retry attempts.
        backoff: Backoff (seconds).

    Returns:
        The wrapped function.

    Raises:
        Exception: Maximum no. of retry attempts exceeded.
    """
    def wrapper(*args, **kwargs):
        c = 0
        while True:
            try:
                return f(*args, **kwargs)
            except:
                if c == retries:
                    raise Exception(f"Maximum retries ({retries}) exceeded.")
                else:
                    time.sleep(backoff * 2**c)
                    c += 1
    return wrapper
