import pytest

from comparaison import (actions_rachetees, options_nettes, spcx_part_capital_musk, tableau_comparatif)
from donnees import charger_prospectus
from comparaison import DATA


def test_rachat_options_dans_la_monnaie():
    # 100 options à 20 $, cours 100 $ : 2 000 $ encaissés rachètent 20 actions
    assert actions_rachetees(100, 20, 100) == pytest.approx(20)
    assert options_nettes(100, 20, 100) == pytest.approx(80)


def test_options_hors_de_la_monnaie_sans_effet():
    assert options_nettes(100, 120, 100) == 0


def test_capitalisations_ipo():
    t = tableau_comparatif()
    assert t.loc["capitalisation_diluee_ipo", "ANT"] == pytest.approx(1505.4e9, rel=1e-3)
    assert t.loc["capitalisation_base_ipo", "SPCX"] == pytest.approx(1776.5e9, rel=1e-3)


def test_premier_jour():
    t = tableau_comparatif()
    assert t.loc["rendement_cloture_j1", "ANT"] == pytest.approx(0.1707, abs=1e-3)
    assert t.loc["rendement_cloture_j1", "SPCX"] == pytest.approx(0.1922, abs=1e-3)


def test_part_capital_musk():
    s = charger_prospectus(DATA / "spacex.csv")
    assert spcx_part_capital_musk(s) == pytest.approx(0.463, abs=0.005)
