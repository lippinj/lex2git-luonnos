from dataclasses import dataclass
from finlaw.elements import Element


@dataclass
class Address:
    chapter: int | None
    section: int
    paragraph: int | None


class Statute:
    def __init__(self, elements: [Element]):
        self.elements = elements

    def find(self, addr: Address) -> (int, int):
        pass

    def repeal(self, addr: Address) -> None:
        pass

    def replace(self, addr: Address, new: [Element]) -> None:
        pass

    def insert(self, addr: Address, new: [Element]) -> None:
        i, j = self.find(addr)