import re
from finlaw.list_form import ItemType, Item, ListForm


def load(path: str) -> ListForm:
    with open(path, "r", encoding="utf-8") as f:
        return parse(f)


def dump(path: str, lf: ListForm) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(compose(lf))


def parse(seq) -> ListForm:
    if isinstance(seq, str):
        seq = seq.split("\n")
    return ListForm([parse_one(s) for s in seq if s.strip()])


def compose(lf: ListForm) -> None:
    return "\n\n".join(compose_one(e) for e in lf.items) + "\n"


def parse_one(s: str) -> Item:
    s = s.strip()
    if m := re.match(r"# (.+)", s):
        return Item(ItemType.Nimike, None, m.group(1))
    if m := re.match(r"## ([IVX]+) OSA<br>(.+)", s):
        return Item(ItemType.Osa, m.group(1), m.group(2))
    if m := re.match(r"### (\d+) luku<br>(.+)", s):
        return Item(ItemType.Luku, int(m.group(1)), m.group(2))
    if m := re.match(r"#### (\d+) §<br>(.+)", s):
        return Item(ItemType.Pykälä, int(m.group(1)), m.group(2))
    if m := re.match(r"(\d+)\) (.+)", s):
        return Item(ItemType.Kohta, int(m.group(1)), m.group(2))
    return Item(ItemType.Kappale, None, s)


def compose_one(item: Item) -> str:
    match item.type:
        case ItemType.Nimike:
            return f"# {item.text}"
        case ItemType.Osa:
            return f"## {item.number} OSA<br>{item.text}"
        case ItemType.Luku:
            return f"### {item.number} luku<br>{item.text}"
        case ItemType.Pykälä:
            return f"#### {item.number} §<br>{item.text}"
        case ItemType.Kohta:
            return f"{item.number}) {item.text}"
        case ItemType.Kappale:
            return item.text
        case _:
            raise NotImplementedError(f"Unknown item type {item.type}")
