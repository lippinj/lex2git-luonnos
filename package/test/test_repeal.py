import pytest
import common
from finlaw.serialization import markdown
from finlaw.list_form import ItemType, Item, ListForm


def test_yksinkertaisen_momentin_kumoaminen():
    L = markdown.load(common.data_path("2002.1290.md"))

    L.repeal("1.2.3")
    assert L[8] == Item(ItemType.Kappale, None, "Työmarkkinatukea maksetaan työnhakijalle, joka ei ole ollut vakiintuneesti työmarkkinoilla tai on saanut työttömyyspäivärahaa enimmäisajan. Vakiintuneesti työmarkkinoilla olleelle ja palkkatyöstä, yritystoiminnasta tai siihen rinnastettavasta omasta työstä toimeentulon saaneelle työnhakijalle maksetaan työttömyyspäivärahaa. Työttömyyspäiväraha maksetaan työttömyyskassalaissa (603/1984) tarkoitetussa työttömyyskassassa vakuutettuina oleville ansiopäivärahana ja muille peruspäivärahana.")
    assert L[9] == Item(ItemType.Tyhjä, None, None)
    assert L[10] == Item(ItemType.Pykälä, 3, "Etuuden saajan yleiset oikeudet ja velvollisuudet")


def test_kohtiin_jaetun_momentin_kumoaminen():
    L = markdown.load(common.data_path("2002.1290.md"))

    L.repeal("5.4.5")
    assert L[249] == Item(ItemType.Kappale, None, "Työssäoloehtoon luetaan puolet niiden kalenteriviikkojen lukumäärästä, joina tehdyn työn palkkauskustannuksiin työnantaja on saanut samalta ajalta työmarkkinatukea ja julkisesta työvoimapalvelusta annetussa laissa tarkoitettua työllistämistukea.")
    assert L[250] == Item(ItemType.Tyhjä, None, None)
    assert L[251] == Item(ItemType.Kappale, None, "Edellä 5 momentissa tarkoitettu työaikaedellytyksen täyttyminen määritellään siten, että työtulojen tai työajan perustella määritellään toiminnan olennaisuus työttömyysturvan kannalta.")