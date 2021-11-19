class Karma:
    _value: int

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def enough_for_voting(self) -> bool:
        return self._value >= 5
