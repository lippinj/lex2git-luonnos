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

    def __repr__(self) -> str:
        match self.type:
            case ItemType.Nimike:
                return f"<# {self.text}>"
            case ItemType.Osa:
                return f"<{self.number} OSA: {self.text}>"
            case ItemType.Luku:
                return f"<{self.number} luku: {self.text}>"
            case ItemType.Pykälä:
                return f"<{self.number} §: {self.text}>"
            case ItemType.Kappale:
                return f"<{self.text}>"
            case ItemType.Kohta:
                return f"<{self.number}) {self.text}>"
            case ItemType.Tyhjä:
                return f"<>"
            case _:
                raise NotImplementedError


class Address:
    def __init__(self, spec: tuple|str):
        if isinstance(spec, str):
            spec = tuple(int(e) for e in spec.split("."))

        assert len(spec) in (1, 2, 3, 4), spec
        assert any(e >= 1 for e in spec), spec

        self.luku = spec[0]
        self.pykälä = None if (len(spec) < 2) else spec[1]
        self.momentti = None if (len(spec) < 3) else spec[2]
        self.kohta = None if (len(spec) < 4) else spec[3]

    def prev(self):
        if self.kohta:
            assert self.kohta > 1
            return Address((self.luku, self.pykälä, self.momentti, self.kohta - 1))
        elif self.momentti:
            assert self.momentti > 1
            return Address((self.luku, self.pykälä, self.momentti - 1, self.kohta))
        else:
            raise ValueError


class ListForm:
    def __init__(self, items: [Item] = None):
        self.items = items or []

    def __len__(self):
        return len(self.items)

    def __getitem__(self, ind):
        return self.items[ind]

    def find(self, addr: Address|tuple|str) -> (int, int):
        addr = addr if isinstance(addr, Address) else Address(addr)
        start, stop = self._find_luku(addr.luku)
        if addr.pykälä:
            start, stop = self._find_pykälä(addr.pykälä, start, stop + 1)
        if addr.momentti:
            start, stop = self._find_momentti(addr.momentti, start, stop + 1)
        if addr.kohta:
            start, stop = self._find_kohta(addr.kohta, start, stop + 1)
        return (start, stop)

    def repeal(self, addr: Address|tuple|str):
        addr = addr if isinstance(addr, Address) else Address(addr)
        if addr.kohta:
            raise NotImplementedError
        if addr.momentti:
            start, stop = self.find(addr)
            del self.items[start:stop+1]
            self.items.insert(start, Item(ItemType.Tyhjä, None, None))
        elif addr.pykälä:
            start, stop = self.find(addr.pykälä)
            if stop > start:
                del self.items[start+1:stop+1]
        else:
            raise ValueError("Can't repeal Luku")

    def insert(self, addr: Address|tuple|str, item: Item):
        addr = addr if isinstance(addr, Address) else Address(addr)
        if addr.kohta:
            assert item.number == addr.kohta
            try:
                start, stop = self.find(addr)
                self.items.insert(start, item)
            except IndexError:
                start, stop = self.find(addr.prev())
                self.items.insert(stop + 1, item)
        elif addr.momentti:
            try:
                start, stop = self.find(addr)
                self.items.insert(start, item)
            except IndexError:
                start, stop = self.find(addr.prev())
                self.items.insert(stop + 1, item)
        else:
            raise NotImplementedError

    def change(self, addr: Address|tuple|str, item: Item):
        addr = addr if isinstance(addr, Address) else Address(addr)
        if addr.kohta or addr.momentti:
            start, stop = self.find(addr)
            if start < stop:
                del self.items[start+1:stop+1]
            self.items[start] = item
        else:
            raise NotImplementedError

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
        raise IndexError(f"Could not find Pykälä #{n}")

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
        raise IndexError(f"Could not find Momentti #{n}")

    def _find_momentti_stop(self, begin: int, end: int) -> int:
        for i in range(begin, end):
            if self[i].type in (ItemType.Osa, ItemType.Luku, ItemType.Pykälä, ItemType.Kappale):
                return i - 1
        return end - 1

    def _find_kohta(self, n: int, begin: int, end: int) -> (int, int):
        start = self._find_kohta_start(n, begin, end)
        stop = self._find_kohta_stop(start + 1, end)
        assert stop >= start
        return (start, stop)

    def _find_kohta_start(self, n: int, begin: int, end: int) -> int:
        k = 1
        for i in range(begin, end):
            it = self[i]
            if it.type == ItemType.Kohta:
                if k == n:
                    return i
                else:
                    k += 1
        raise IndexError(f"Could not find kohta #{n}")

    def _find_kohta_stop(self, begin: int, end: int) -> int:
        for i in range(begin, end):
            if self[i].type in (ItemType.Osa, ItemType.Luku, ItemType.Pykälä, ItemType.Kappale, ItemType.Kohta):
                return i - 1
        return end - 1
