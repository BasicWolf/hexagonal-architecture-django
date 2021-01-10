from typing import NoReturn


def assert_never(v: NoReturn) -> NoReturn:
    raise AssertionError(f"Invalid value: {v!r}")
