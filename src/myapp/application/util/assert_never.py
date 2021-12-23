from typing import Any, NoReturn


def assert_never(v: Any) -> NoReturn:
    raise AssertionError(f"Invalid value: {v!r}")
