from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    Nimike = 0
    Osa = 1
    Luku = 2
    Pykälä = 3
    Teksti = 4
    Tyhjä = 5


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

    def __getitem__(self, ind):
        return self.items[ind]

    def find(self, address) -> (int, int):
        luku, pykälä, momentti = address
        start, end = self._find_luku(luku)
        if pykälä:
            start, end = self._find_pykälä(pykälä, (start, end + 1))
        if momentti:
            start, end = self._find_momentti(momentti, (start, end + 1))
        return (start, end)

    def repeal(self, address):
        i = self.find(address)
        self.items[i] = Item(ItemType.Tyhjä, None, None)

    def _find_luku(self, n) -> (int, int):
        start = None
        i = 0
        for i in range(len(self)):
            item = self[i]
            if (item.type == ItemType.Luku) and (item.number == n):
                start = i
                break
        if start is None:
            raise IndexError
        for i in range(start + 1, len(self)):
            item = self[i]
            if item.type in (ItemType.Osa, ItemType.Luku):
                return (start, i - 1)
        return (start, len(self) - 1)

    def _find_pykälä(self, n, span) -> (int, int):
        start = None
        i = 0
        for i in range(*span):
            item = self[i]
            if (item.type == ItemType.Pykälä) and (item.number == n):
                start = i
                break
        if start is None:
            raise IndexError
        for i in range(start + 1, span[1]):
            item = self[i]
            if item.type in (ItemType.Osa, ItemType.Luku, ItemType.Pykälä):
                return (start, i - 1)
        return (start, span[1] - 1)

    def _find_momentti(self, pykälä, span) -> (int, int):
        raise NotImplementedError