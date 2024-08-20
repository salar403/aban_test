import time
from django.core.cache import caches
from functools import wraps
from backend.customs.exceptions import LockedKeyException

cache = caches["cache_lock"]


def generate_key(function_name, **kwargs):
    keywords = "".join(f"{key}_{kwargs[key]}" for key in kwargs)
    return f"{function_name}_{keywords}"


def accuire_lock(key, expire: float = None):
    return cache.add(key, True, expire)


def release_lock(key):
    return cache.delete(key)


def locked_process(
    expire_time: float = None,
    hold: bool = False,
    failwait: float = 10,
):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            free = False
            key = generate_key(function_name=func.__name__, **kwargs)
            if not accuire_lock(key=key, expire=expire_time):
                start_time = time.time()
                if not hold:
                    raise LockedKeyException(code="duplicated_process")
                while time.time() - start_time <= failwait:
                    if accuire_lock(key=key, expire=expire_time):
                        free = True
                        break
                    time.sleep(0.05)
                if not free:
                    raise LockedKeyException(code="duplicated_process")
            try:
                result = func(*args, **kwargs)
                release_lock(key=key)
                return result
            except:
                release_lock(key=key)
                raise

        return wrapper

    return decorate
