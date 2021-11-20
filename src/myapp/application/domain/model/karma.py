from dataclasses import dataclass


@dataclass
class Karma:
    value: int

    def enough_for_voting(self) -> bool:
        return self.value >= 5

    def __str__(self):
        return f"Karma({self.value})"
