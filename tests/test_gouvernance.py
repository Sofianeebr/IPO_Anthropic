import pytest

from gouvernance import repartition, voix_des_cofondateurs


def test_les_parts_font_100_pourcent():
    tableau = repartition()
    assert tableau["part_capital"].sum() == pytest.approx(1)
    assert tableau["part_voix"].sum() == pytest.approx(1)


def test_cofondateurs_environ_61_pourcent_des_voix():
    assert voix_des_cofondateurs(repartition()) == pytest.approx(0.613, abs=0.002)


def test_public_environ_6_pourcent_du_capital():
    tableau = repartition().set_index("groupe")
    assert tableau.loc["Public (actions de l'IPO)", "part_capital"] == pytest.approx(0.063, abs=0.001)
