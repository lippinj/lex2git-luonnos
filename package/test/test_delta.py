import pytest
import common
from finlaw.serialization import markdown
from finlaw.list_form import Address, ItemType, Item, ListForm
from finlaw.delta import Delta, DeltaSet


def test_deltan_parsiminen():
    L = markdown.load(common.data_path("2003.39.md"))
    d = DeltaSet.parse_list_form(L)
    assert len(d) == 1
    assert d[0] == Delta(Action.Insert, Address("15.1.12"), Item.Momentti("Sen estämättä, mitä tämän lain 9 luvun 6 §:n 1 momentissa säädetään, 1 päivän tammikuuta ja 30 päivän kesäkuuta 2003 välisenä aikana työmarkkinatuki on kuitenkin 60 prosenttia sanotun momentin mukaisesti lasketusta työmarkkinatuesta."))


def test_clean_paragraph():
    text = "_lisätään_ 30 päivänä joulukuuta 2002 annetun työttömyysturvalain (1290/2002) 15 luvun 1 §:ään uusi 12 momentti, jolloin nykyinen 12―15 momentti siirtyvät 13―16 momentiksi, seuraavasti:"
    action, text, act = DeltaSet.clean_paragraph(text)
    assert action == "lisätään"
    assert text == "15 luvun 1 §:ään uusi 12 momentti, jolloin nykyinen 12―15 momentti siirtyvät 13―16 momentiksi"
    assert act == "1290/2002"