"""Comparaison des introductions en Bourse d'Anthropic (ANT, 19/11/2026) et de SpaceX (SPCX, 12/06/2026).

Toutes les données viennent des prospectus définitifs (424B4) et des cours yfinance.
"""
from pathlib import Path

import pandas as pd

from donnees import charger_prospectus
from marche import argent_laisse_sur_la_table, rendement

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "data"


def actions_rachetees(nb_options, prix_exercice, prix):
    """Méthode du rachat d'actions (treasury stock method).

    La société encaisse nb_options x prix_exercice et s'en sert pour racheter des actions au prix de marché.
    Si l'option est hors de la monnaie (prix_exercice > prix), elle n'est pas exercée : on renvoie nb_options.
    """
    if prix_exercice >= prix:
        return nb_options
    return nb_options * prix_exercice / prix


def options_nettes(nb_options, prix_exercice, prix):
    """Actions nouvelles réellement créées par les options, après rachat."""
    return nb_options - actions_rachetees(nb_options, prix_exercice, prix)


# ---------- Anthropic ----------

# La greenshoe d'Anthropic n'est pas encore confirmée comme exercée au 20/11/2026 : on l'exclut.
# Celle de SpaceX a été exercée en totalité (communiqué du 15/06/2026) : on l'inclut.

def ant_actions_base(d):
    return d["actions_total_apres_ipo"]


def ant_actions_diluees(d):
    """Base diluée du tableau de dilution du 424B4. T et F exclues (pas de droits économiques)."""
    return d["dil_actions_A_total"] + d["dil_actions_N_total"] + d["dil_options_nettes"] + d["dil_rsu_total"]


# ---------- SpaceX ----------

def spcx_actions_base(s):
    return s["actions_A_apres_ipo_avec_greenshoe"] + s["actions_B_apres_ipo"]


def spcx_actions_diluees(s, prix):
    return (
        spcx_actions_base(s)
        + options_nettes(s["exclu_options_A"], s["exclu_options_A_prix_exercice"], prix)
        + options_nettes(s["exclu_options_B"], s["exclu_options_B_prix_exercice"], prix)
        + s["exclu_rsu_A"] + s["exclu_rsu_B"]
    )


def spcx_part_capital_musk(s):
    """Estimation de la part du capital d'Elon Musk à partir de ses parts de voix.

    V = voix totales (1 par action A, 10 par action B).
    Actions B de Musk = part de voix via les B x V / 10.
    Actions A de Musk = (part de voix totale moins part via les B) x V.
    """
    voix_totales = s["actions_A_apres_ipo"] + s["actions_B_apres_ipo"] * s["voix_par_action_B"]
    actions_b = s["part_voix_actions_B_elon_musk"] * voix_totales / s["voix_par_action_B"]
    actions_a = (s["part_voix_elon_musk"] - s["part_voix_actions_B_elon_musk"]) * voix_totales
    return (actions_a + actions_b) / (s["actions_A_apres_ipo"] + s["actions_B_apres_ipo"])


# ---------- Tableau comparatif ----------

def tableau_comparatif():
    d = charger_prospectus(DATA / "ipo_definitive.csv")
    s = charger_prospectus(DATA / "spacex.csv")
    pj = pd.read_csv(DATA / "premier_jour.csv", index_col="ticker")
    tri = pd.read_csv(DATA / "trimestres_anthropic.csv", index_col="poste")
    ca_ant_12m = tri.loc["chiffre_affaires", ["T4_2025", "T1_2026", "T2_2026", "T3_2026"]].sum()
    ca_spcx_12m = s["chiffre_affaires_2025"] - s["chiffre_affaires_T1_2025"] + s["chiffre_affaires_T1_2026"]

    lignes = {}
    for ticker, prix, base, dilue, ca12, flottant in [
        ("ANT", d["prix_ipo"], ant_actions_base(d), ant_actions_diluees(d), ca_ant_12m,
         d["actions_A_offertes_total"]),
        ("SPCX", s["prix_ipo"], spcx_actions_base(s), spcx_actions_diluees(s, s["prix_ipo"]), ca_spcx_12m,
         s["actions_A_offertes"] + s["actions_A_greenshoe"]),
    ]:
        jour = pj.loc[ticker]
        lignes[ticker] = {
            "prix_ipo": prix,
            "actions_base": base,
            "actions_diluees": dilue,
            "capitalisation_base_ipo": prix * base,
            "capitalisation_diluee_ipo": prix * dilue,
            "capitalisation_diluee_cloture_j1": jour["cloture"] * dilue,
            "flottant": flottant / base,
            "rendement_ouverture_j1": rendement(prix, jour["ouverture"]),
            "rendement_cloture_j1": rendement(prix, jour["cloture"]),
            "argent_laisse_sur_la_table": argent_laisse_sur_la_table(prix, jour["cloture"], jour["actions_offertes"]),
            "rotation_flottant_j1": jour["volume"] / flottant,
            "ca_12_derniers_mois": ca12 * 1e6,
            "capitalisation_diluee_sur_ca": prix * dilue / (ca12 * 1e6),
        }
    return pd.DataFrame(lignes)


def parcours_depuis_ipo(ticker, prix_ipo):
    """Cours de clôture divisé par le prix d'IPO, indexé par le nombre de séances depuis la cotation."""
    cours = pd.read_csv(DATA / f"cours_{ticker}.csv", index_col=0, parse_dates=True)
    serie = cours["Close"] / prix_ipo
    return pd.Series(serie.values, index=range(len(serie)), name=ticker)


if __name__ == "__main__":
    pd.set_option("display.float_format", lambda x: f"{x:,.3f}")
    print(tableau_comparatif())
    s = charger_prospectus(DATA / "spacex.csv")
    print("Part du capital de Musk (estimation) :", round(spcx_part_capital_musk(s), 3))
