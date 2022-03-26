from typing import Protocol, TypeVar

T_contra = TypeVar('T_contra', contravariant=True)


class Specification(Protocol[T_contra]):
    def is_satisfied_by(self, obj: T_contra) -> bool:
        raise NotImplementedError()
