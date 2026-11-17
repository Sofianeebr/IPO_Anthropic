"""Vérifie que les calculs retrouvent les chiffres du prospectus S-1/A n°2 du 10/11/2026 (prix médian de 74 $)."""
import pytest

from donnees import charger_prospectus
from valorisation import actions_diluees, actions_non_diluees, actions_rachetees_options

donnees = charger_prospectus("data/prospectus.csv")


def test_base_non_diluee_au_prix_median():
    """Total d'actions après l'IPO de la section The Offering (écart dû à l'arrondi par partenaire du placement privé)."""
    assert actions_non_diluees(74, donnees) == pytest.approx(13_086_672_593, abs=10)


def test_base_diluee_au_prix_median():
    """Total du tableau de dilution page 24 (18 012 993 381), sans les 2 actions T et F sans droit économique."""
    assert actions_diluees(74, donnees) == pytest.approx(18_012_993_379, abs=10)


def test_rachat_options_au_prix_median():
    """Actions rachetées par la méthode du rachat d'actions, tableau page 24."""
    assert actions_rachetees_options(74, donnees) == pytest.approx(69_774_828, abs=1)


def test_base_diluee_baisse_quand_le_prix_monte():
    """Un prix plus élevé réduit les actions du placement privé et les options nettes."""
    assert actions_diluees(85, donnees) < actions_diluees(74, donnees) < actions_diluees(70, donnees)
