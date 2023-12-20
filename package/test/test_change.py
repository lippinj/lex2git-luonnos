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


def test_kohdan_muuttaminen():
    L = markdown.load(common.data_path("2002.1290.md"))

    item = Item(ItemType.Kohta, 10, "_työnhakusuunnitelmalla_ julkisesta työvoimapalvelusta annetun lain mukaista työttömän työnhakijan työllistymisedellytysten selvittämiseksi ja niiden parantamiseksi laadittua suunnitelmaa;")
    L.change((1, 5, 1, 10), item)
    assert L[27] == Item(ItemType.Kohta, 9, "_työssäolovelvoitteella_ työssä- tai koulutuksessaoloa, joka edellytetään ennen kuin työttömyysetuutta voidaan maksaa toistuvan 8 kohdassa tarkoitetun työhaluttomuutta osoittavan menettelyn johdosta, tai joka edellytetään ennen kuin työmarkkinatukea voidaan maksaa työttömyysajalta 8 luvun 2 §:n 3 momentissa tarkoitetun menettelyn johdosta;")
    assert L[28] == item
    assert L[29] == Item(ItemType.Kohta, 11, "_yhdistelmätuella_ pitkään työttömänä olleen työllistymisen edistämiseksi tarkoitettua tukea, jossa työmarkkinatuki voidaan määrätä maksettavaksi työnantajalle joko yksinään tai yhdistettynä julkisesta työvoimapalvelusta annetussa laissa tarkoitettuun työllistämistukeen.")
