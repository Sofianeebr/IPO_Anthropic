import pytest

from finances import (bfr_exploitation, charger_bilan, charger_etats, charger_trimestres,
                      chiffre_affaires_annuel, croissance, diagnostic)


def test_croissance():
    assert croissance(150, 100) == pytest.approx(0.5)


def test_caf_9m2026():
    d = diagnostic(charger_etats())
    assert d.loc["9M2026", "caf"] == pytest.approx(6142)


def test_caf_moins_variation_bfr_donne_flux_exploitation():
    # Tableau de flux : flux d'exploitation = CAF + variation de BFR (signe du tableau de flux)
    d = diagnostic(charger_etats())
    for periode in d.index:
        assert d.loc[periode, "caf"] + d.loc[periode, "variation_bfr"] == pytest.approx(
            d.loc[periode, "flux_tresorerie_exploitation"]
        )


def test_flux_disponible_9m2026():
    d = diagnostic(charger_etats())
    assert d.loc["9M2026", "flux_disponible"] == pytest.approx(3689)


def test_chiffre_affaires_12_mois():
    r = chiffre_affaires_annuel(charger_trimestres())
    assert r["quatre_derniers_trimestres"] == 35282
    assert r["dernier_trimestre_annualise"] == 67824


def test_bfr_exploitation_negatif():
    assert bfr_exploitation(charger_bilan()) == -2222
