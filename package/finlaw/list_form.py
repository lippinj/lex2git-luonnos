from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    Nimike = 0
    Osa = 1
    Luku = 2
    Pykälä = 3
    Kappale = 4
    Kohta = 5
    Tyhjä = 6


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
        start, stop = self._find_luku(luku)
        if pykälä:
            start, stop = self._find_pykälä(pykälä, start, stop + 1)
        if momentti:
            start, stop = self._find_momentti(momentti, start, stop + 1)
        return (start, stop)

    def repeal(self, address):
        luku, pykälä, momentti = address
        if momentti:
            start, stop = self.find(address)
            del self.items[start:stop+1]
            self.items.insert(start, Item(ItemType.Tyhjä, None, None))
        elif pykälä:
            start, stop = self.find(pykälä)
            if stop > start:
                del self.items[start+1:stop+1]
        else:
            raise ValueError("Can't repeal Luku")

    def _find_luku(self, n: int) -> (int, int):
        start = self._find_luku_start(n, 0, len(self))
        stop = self._find_luku_stop(start + 1, len(self))
        assert stop >= start, (start, stop)
        return (start, stop)

    def _find_luku_start(self, n: int, begin: int, end: int) -> int:
        for i in range(begin, end):
            it = self[i]
            if (it.type == ItemType.Luku) and (it.number == n):
                return i
        raise ValueError(f"Could not find Luku #{n}")

    def _find_luku_stop(self, begin: int, end: int) -> int:
        for i in range(begin, end):
            if self[i].type in (ItemType.Osa, ItemType.Luku):
                return i - 1
        return end - 1

    def _find_pykälä(self, n: int, begin: int, end: int) -> (int, int):
        start = self._find_pykälä_start(n, begin, end)
        stop = self._find_pykälä_stop(start + 1, end)
        assert stop >= start
        return (start, stop)

    def _find_pykälä_start(self, n: int, begin: int, end: int) -> int:
        for i in range(begin, end):
            it = self[i]
            if (it.type == ItemType.Pykälä) and (it.number == n):
                return i
        raise ValueError(f"Could not find Pykälä #{n}")

    def _find_pykälä_stop(self, begin: int, end: int) -> int:
        for i in range(begin, end):
            if self[i].type in (ItemType.Osa, ItemType.Luku, ItemType.Pykälä):
                return i - 1
        return end - 1

    def _find_momentti(self, n: int, begin: int, end: int) -> (int, int):
        start = self._find_momentti_start(n, begin, end)
        stop = self._find_momentti_stop(start + 1, end)
        assert stop >= start
        return (start, stop)

    def _find_momentti_start(self, n: int, begin: int, end: int) -> int:
        k = 1
        for i in range(begin, end):
            it = self[i]
            if it.type == ItemType.Kappale:
                if k == n:
                    return i
                else:
                    k += 1
        raise ValueError(f"Could not find Momentti #{n}")

    def _find_momentti_stop(self, begin: int, end: int) -> int:
        for i in range(begin, end):
            if self[i].type in (ItemType.Osa, ItemType.Luku, ItemType.Pykälä, ItemType.Kappale):
                return i - 1
        return end - 1
