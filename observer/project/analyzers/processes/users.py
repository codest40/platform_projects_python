from functools import lru_cache
import pwd
import grp


@lru_cache(maxsize=None)
def get_user(uid: int):
    """Return the passwd entry for a UID."""

    try:
        uid = pwd.getpwuid(uid)
        return uid
    except KeyError:
        return None


@lru_cache(maxsize=None)
def get_group(gid: int):

    try:
        return grp.getgrgid(gid)
    except KeyError:
        return None
