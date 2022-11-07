from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from django.conf import settings
from django.db import transaction

T = TypeVar('T')
P = ParamSpec('P')


def transactional(f: Callable[P, T]) -> Callable[P, T]:
    if settings.TESTING:
        return f
    else:
        @wraps(f)
        def inner(*args: P.args, **kwargs: P.kwargs) -> T:
            with transaction.atomic():
                return f(*args, **kwargs)
        return inner
