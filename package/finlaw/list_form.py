from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    Nimike = 0
    Osa = 1
    Luku = 2
    Pykälä = 3
    Teksti = 4


@dataclass
class Item:
    type: ItemType
    number: int | str | None
    text: str | None


class ListForm:
    def __init__(self, items: [Item] = None):
        self.items = items or []

    def __len__(self):
        return len(self.items)
