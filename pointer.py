from dataclasses import dataclass

@dataclass
class Ref[T]:
    value: T

    def __mul__(self, other: T):
        self.value = other
        return self

    def __getitem__(self, _) -> T:
        return self.value

    def __rmul__(self):
        assert False, "Pointers should only ever be *= or [], all other operations are illegal"

