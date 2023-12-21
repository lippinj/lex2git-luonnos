import re
from dataclasses import dataclass
from enum import Enum
from finlaw.list_form import Address, Item, ListForm


class Action(Enum):
    Repeal = 0
    Change = 1
    Insert = 2


@dataclass
class Delta:
    action: Action
    address: Address
    item: Item|None

    def __repr__(self) -> str:
        return f"<{self.action}{repr(self.address)}:{repr(self.item)}>"

    def apply(self, L: ListForm) -> None:
        match action:
            case '+':
                L.repeal(self.address)
            case '*':
                L.change(self.address, self.item)
            case Action.Insert:
                L.insert(self.address, self.item)
            case _:
                raise NotImplementedError


class DeltaSet:
    def __init__(self, deltas: [Delta] = None):
        self.deltas = deltas or []

    def __len__(self) -> int:
        return len(self.deltas)

    def __getitem__(self, idx: int) -> Delta:
        if isinstance(idx, tuple):
            return self.deltas[idx[0]:idx[1]+1]
        return self.deltas[idx]

    @staticmethod
    def parse_list_form(L: ListForm):
        act, clauses = DeltaSet.clean_paragraphs(L)
        
        actions = []
        for action, text in clauses:
            assert action == "lisätään"
            m = re.match(r"(\d+) luvun (\d+) §:ään uusi (\d+) momentti", text)
            if m:
                luku = int(m.group(1))
                pykälä = int(m.group(2))
                momentti = int(m.group(3))
                address = Address((luku, pykälä, momentti))
                actions.append((Action.Insert, address))

    @staticmethod
    def clean_paragraphs(L: ListForm) -> (str, [(str, str)]):
        act = None
        clauses = []
        for item in L[L.find_leader()]:
            text = item.text
            if text.startswith("_"):
                action, text, _act = DeltaSet.clean_paragraph(text)
                if _act:
                    act = _act
                clauses.append((action, text))
        assert act is not None
        assert len(set(a for a, t in clauses)) == len(clauses)
        return act, clauses

    @staticmethod
    def clean_paragraph(text: str) -> (str, str, str|None):
        _, action, text = text.split("_", maxsplit=2)
        text = text.removesuffix("seuraavasti:")
        text = text.removesuffix("ja")
        text = text.strip(" ,")
        act, text = DeltaSet.parse_act(text)
        return action, text, act

    @staticmethod
    def parse_act(text: str) -> (str|None, str):
        m = re.match(r".+\d{4} annetun .+ \((\d+/\d{4})\) (.+)", text)
        if m:
            return m.group(1), m.group(2)
        return None, text
