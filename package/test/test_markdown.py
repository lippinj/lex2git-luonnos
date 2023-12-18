import pytest
import common
from finlaw.serialization import markdown
from finlaw.list_form import ItemType, Item, ListForm


@pytest.mark.parametrize("filename,size", [
    ("2002.1290.md", 726), # Alkuperäinen säädös
    ("2003.39.md", 10), # Muutossäädös
])
def test_säädöksen_parsiminen_ja_koonti(filename, size):
    md = common.read_data(filename)

    L = markdown.parse(md)
    assert isinstance(L, ListForm)
    assert len(L.items) == size

    md_out = markdown.compose(L)
    assert md_out == md


def test_nimikkeen_parsiminen():
    L = markdown.load(common.data_path("2002.1290.md"))
    assert L.items[0] == Item(ItemType.Nimike, None, "Työttömyysturvalaki")

    L = markdown.load(common.data_path("2003.39.md"))
    assert L.items[0] == Item(ItemType.Nimike, None, "Laki työttömyysturvalain 15 luvun 1 §:n muuttamisesta")


def test_osan_parsiminen():
    L = markdown.load(common.data_path("2002.1290.md"))
    assert L.items[2] == Item(ItemType.Osa, "I", "YHTEISET SÄÄNNÖKSET")
    assert L.items[233] == Item(ItemType.Osa, "II", "TYÖTTÖMYYSPÄIVÄRAHA")
    assert L.items[335] == Item(ItemType.Osa, "III", "TYÖMARKKINATUKI")
    assert L.items[493] == Item(ItemType.Osa, "IV", "KOULUTUSPÄIVÄRAHA")
    assert L.items[534] == Item(ItemType.Osa, "V", "TOIMEENPANO JA MUUTOKSENHAKU")
    assert L.items[643] == Item(ItemType.Osa, "VI", "ERINÄISET SÄÄNNÖKSET")


def test_luvun_parsiminen():
    L = markdown.load(common.data_path("2002.1290.md"))
    assert L.items[3] == Item(ItemType.Luku, 1, "Yleiset säännökset")
    assert L.items[49] == Item(ItemType.Luku, 2, "Etuuden saamisen työvoimapoliittiset edellytykset")
    assert L.items[687] == Item(ItemType.Luku, 14, "Erinäisiä säännöksiä")

    L = markdown.load(common.data_path("2003.39.md"))
    assert L.items[3] == Item(ItemType.Luku, 15, "Voimaantulosäädökset")


def test_pykälän_parsiminen():
    L = markdown.load(common.data_path("2002.1290.md"))
    assert L.items[4] == Item(ItemType.Pykälä, 1, "Lain tarkoitus")
    assert L.items[6] == Item(ItemType.Pykälä, 2, "Etuudet")
    assert L.items[17] == Item(ItemType.Pykälä, 5, "Määritelmät")
    assert L.items[703] == Item(ItemType.Pykälä, 1, "Voimaantulo")

    L = markdown.load(common.data_path("2003.39.md"))
    assert L.items[4] == Item(ItemType.Pykälä, 1, "Voimaantulosäädökset")