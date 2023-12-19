import pytest
import common
from finlaw.serialization import markdown
from finlaw.list_form import ItemType, Item, ListForm


def test_luvun_etsiminen():
    L = markdown.load(common.data_path("2002.1290.md"))
    # Luku päättyy seuraavan luvun alkuun
    assert L.find((1, None, None)) == (3, 48)
    assert L.find((2, None, None)) == (49, 151)
    assert L.find((3, None, None)) == (152, 187)
    # Luku päättyy seuraavan osan alkuun
    assert L.find((4, None, None)) == (188, 232)
    # Luku päättyy säädöksen loppuun
    assert L.find((15, None, None)) == (702, 725)


def test_pykälän_etsiminen():
    L = markdown.load(common.data_path("2002.1290.md"))
    # Pykälä päättyy seuraavan pykälän alkuun
    assert L.find((1, 1, None)) == (4, 5)
    assert L.find((1, 2, None)) == (6, 9)
    # Pykälä päättyy seuraavan luvun alkuun
    assert L.find((1, 9, None)) == (46, 48)
    # Pykälä päättyy seuraavan osan alkuun
    assert L.find((4, 8, None)) == (231, 232)
    # Pykälä päättyy säädöksen loppuun
    assert L.find((15, 3, None)) == (724, 725)


def test_yksinkertaisen_momentin_etsiminen():
    L = markdown.load(common.data_path("2002.1290.md"))
    assert L.find((1, 1, 1)) == (5, 5)
    assert L.find((1, 2, 3)) == (9, 9)


def test_kohtiin_jaetun_momentin_etsiminen():
    L = markdown.load(common.data_path("2002.1290.md"))
    assert L.find((5, 4, 5)) == (250, 255)