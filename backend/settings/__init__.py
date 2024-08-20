from .common import *

match PLATFORM:
    case "production":
        from .production import *
    case "local":
        from .local import *
    case _:
        raise ValueError(f"{PLATFORM} is not a valid platform!!")
