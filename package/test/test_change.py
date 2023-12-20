import pytest
import common
from finlaw.serialization import markdown
from finlaw.list_form import ItemType, Item, ListForm


def test_momentin_muuttaminen():
    L = markdown.load(common.data_path("2002.1290.md"))

    item = Item(ItemType.Kappale, None, "Koulutuspäivärahaan ei sovelleta 6 luvun 3 §:n 3 momenttia eikä 9 luvun 3, 4 ja 6 §:ää. Koulutuspäivärahaa maksetaan 6 luvun 2 §:n 2 momentin mukaisesti korotettuna myös sellaiselle henkilölle, joka on saanut ansiopäivärahan korotettua ansio-osaa 150 päivältä.")
    L.change((10, 5, 2), item)
    assert L[516] == Item(ItemType.Kappale, None, "Koulutuksen ajalta opiskelijalla on oikeus koulutuspäivärahaan. Koulutuspäivärahana maksetaan sitä tämän lain mukaista työttömyysetuutta, jota koskevia säännöksiä henkilöön sovellettaisiin hänen työttömänä ollessaan.")
    assert L[517] == item
    assert L[518] == Item(ItemType.Pykälä, 6, "Koulutuspäivärahakauden kesto")