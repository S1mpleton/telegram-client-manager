from typing import Annotated

from fastapi import Header, HTTPException


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def get_user_id_from_header(x_user_id: Annotated[int, Header()] = None):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-user-D header is missing")

    try:
        user_id = int(x_user_id)
        return user_id

    except ValueError:
        raise HTTPException(status_code=400, detail="X-user-D must be a valid integer")
