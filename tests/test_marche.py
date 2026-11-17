"""Vérifie les mesures du premier jour sur un exemple fictif (l'action ANT n'est pas encore cotée)."""
import pandas as pd
import pytest

from marche import argent_laisse_sur_la_table, bilan_premier_jour, rendement


def test_rendement():
    assert rendement(74, 92.5) == pytest.approx(0.25)


def test_argent_laisse_sur_la_table():
    # 10 $ de hausse sur 825 millions d'actions = 8,25 milliards de dollars
    assert argent_laisse_sur_la_table(74, 84, 825_000_000) == pytest.approx(8.25e9)


def test_bilan_premier_jour_sur_un_exemple_fictif():
    cours = pd.DataFrame(
        {"Open": [90.0, 95.0], "High": [99.0, 97.0], "Low": [85.0, 91.0], "Close": [92.5, 93.0], "Volume": [1e8, 5e7]},
        index=pd.to_datetime(["2026-11-19", "2026-11-20"]),
    )
    resultat = bilan_premier_jour(74, cours)
    assert resultat["rendement_ouverture"] == pytest.approx(16 / 74)
    assert resultat["rendement_premier_jour"] == pytest.approx(0.25)
