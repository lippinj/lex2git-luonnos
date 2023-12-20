import pytest
import common
from finlaw.serialization import markdown
from finlaw.list_form import ItemType, Item, ListForm


def test_momentin_lisääminen_loppuun():
    L = markdown.load(common.data_path("2002.1290.md"))

    item = Item(ItemType.Kappale, None, "Viikoittaisen työajan lyhentämisenä ei pidetä sääesteestä johtuvaa työajan lyhentymistä, jossa työnteko estyy yhdeltä tai useammalta päivältä. Pakkasraja, jolloin sääeste on olemassa, määritetään rakennusalalla ennen työn aloittamista työmaakohtaisesti rakennustyövaihe ja työmaan muut olosuhteet huomioon ottaen. Vastaavasti metsäalalla voidaan etukäteen tarvittaessa määrittää sääesteeksi pakkasraja, jolloin ulkona työskentelyä ei voida kohtuudella vaatia.")
    L.insert("4.1.2", item)
    assert L[194] == Item(ItemType.Kohta, 4, "jolla on tuloa 1 luvun 6 §:n mukaisesta yritystoiminnasta tai omasta työstä.")
    assert L[195] == item
    assert L[196] == Item(ItemType.Pykälä, 2, "Sovittelujakso")


def test_momentin_lisääminen_väliin():
    L = markdown.load(common.data_path("2002.1290.md"))

    item = Item(ItemType.Kappale, None, "Sen estämättä, mitä tämän lain 9 luvun 6 §:n 1 momentissa säädetään, 1 päivän tammikuuta ja 30 päivän kesäkuuta 2003 välisenä aikana työmarkkinatuki on kuitenkin 60 prosenttia sanotun momentin mukaisesti lasketusta työmarkkinatuesta.")
    L.insert("15.1.12", item)
    assert L[714] == Item(ItemType.Kappale, None, "Lain 9 luvun 5 §:n 2 momentissa tarkoitettuun työssäoloehtoon luetaan myös ennen tämän lain voimaantuloa tehty työ tai harjoitettu yritystoiminta.")
    assert L[715] == item
    assert L[716] == Item(ItemType.Kappale, None, "Tämän lain voimaantulon jälkeen alkavaan koulutukseen myönnettävä koulutuspäiväraha määräytyy siten kuin 6 luvun 3 §:ssä säädetään.")


def test_kohdan_lisääminen_loppuun():
    L = markdown.load(common.data_path("2002.1290.md"))

    item = Item(ItemType.Kohta, 12, "_sääesteellä_ työsuhteessa rakennus- ja metsäalalla tapahtuvan työn suorittamisen estymistä, joka johtuu yksinomaan ja välittömästi pakkasesta ja jonka johdosta työnantajalla ei ole työsopimuslain 2 luvun 12 §:n 2 momentin mukaista palkanmaksuvelvollisuutta.")
    L.insert("1.5.1.12", item)
    assert L[29] == Item(ItemType.Kohta, 11, "_yhdistelmätuella_ pitkään työttömänä olleen työllistymisen edistämiseksi tarkoitettua tukea, jossa työmarkkinatuki voidaan määrätä maksettavaksi työnantajalle joko yksinään tai yhdistettynä julkisesta työvoimapalvelusta annetussa laissa tarkoitettuun työllistämistukeen.")
    assert L[30] == item
    assert L[31] == Item(ItemType.Kappale, None, "Tätä lakia sovellettaessa virkasuhteessa tehtävä työ ja virkasuhteeseen liittyvä asia rinnastetaan työsuhteeseen ja työsopimusasiaan.")
