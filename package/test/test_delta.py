import pytest
import common
from finlaw.serialization import markdown
from finlaw.list_form import Address, ItemType, Item, ListForm
from finlaw.delta import Action, Delta, DeltaSet


def test_deltan_parsiminen():
    p0 = common.paragraph("""
        Sen estämättä, mitä tämän lain 9 luvun 6 §:n 1 momentissa säädetään,
        1 päivän tammikuuta ja 30 päivän kesäkuuta 2003 välisenä aikana
        työmarkkinatuki on kuitenkin 60 prosenttia sanotun momentin mukaisesti
        lasketusta työmarkkinatuesta.
    """)

    L = markdown.load(common.data_path("2003.39.md"))
    d = DeltaSet.parse_list_form(L)
    assert d[0] == Delta(Action.Insert, Address("15.1.12"), Item.Kappale(p0))


def test_build_deltas():
    p0 = common.paragraph("""
        Sen estämättä, mitä tämän lain 9 luvun 6 §:n 1 momentissa säädetään,
        1 päivän tammikuuta ja 30 päivän kesäkuuta 2003 välisenä aikana
        työmarkkinatuki on kuitenkin 60 prosenttia sanotun momentin mukaisesti
        lasketusta työmarkkinatuesta.
    """)

    L = markdown.load(common.data_path("2003.39.md"))
    actions = [(Action.Insert, Address("15.1.12"))]
    deltas = DeltaSet.build_deltas(L, actions)
    assert deltas == [
        Delta(Action.Insert, Address("15.1.12"), Item.Kappale(p0)),
    ]


def test_clean_paragraphs():
    p0 = common.paragraph("""
        15 luvun 1 §:ään uusi 12 momentti, jolloin nykyinen 12―15 momentti
        siirtyvät 13―16 momentiksi
    """)
    L = markdown.load(common.data_path("2003.39.md"))
    act, clauses = DeltaSet.clean_paragraphs(L)
    assert act == "1290/2002"
    assert clauses == [("lisätään", p0)]


def test_clean_paragraph():
    p0 = common.paragraph("""
        _lisätään_ 30 päivänä joulukuuta 2002 annetun työttömyysturvalain
        (1290/2002) 15 luvun 1 §:ään uusi 12 momentti, jolloin nykyinen 12―15
        momentti siirtyvät 13―16 momentiksi, seuraavasti:
    """)
    p1 = common.paragraph("""
        15 luvun 1 §:ään uusi 12 momentti, jolloin nykyinen 12―15 momentti
        siirtyvät 13―16 momentiksi
    """)

    action, text, act = DeltaSet.clean_paragraph(p0)
    assert action == "lisätään"
    assert act == "1290/2002"
    assert text == p1