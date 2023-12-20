import pytest
import common
from finlaw.serialization import markdown
from finlaw.list_form import ItemType, Item, ListForm


def test_momentin_lisääminen():
    L = markdown.load(common.data_path("2002.1290.md"))

    item = Item(ItemType.Kappale, None, "Sen estämättä, mitä tämän lain 9 luvun 6 §:n 1 momentissa säädetään, 1 päivän tammikuuta ja 30 päivän kesäkuuta 2003 välisenä aikana työmarkkinatuki on kuitenkin 60 prosenttia sanotun momentin mukaisesti lasketusta työmarkkinatuesta.")
    L.insert("15.1.12", item)
    assert L[714] == Item(ItemType.Kappale, None, "Lain 9 luvun 5 §:n 2 momentissa tarkoitettuun työssäoloehtoon luetaan myös ennen tämän lain voimaantuloa tehty työ tai harjoitettu yritystoiminta.")
    assert L[715] == item
    assert L[716] == Item(ItemType.Kappale, None, "Tämän lain voimaantulon jälkeen alkavaan koulutukseen myönnettävä koulutuspäiväraha määräytyy siten kuin 6 luvun 3 §:ssä säädetään.")
