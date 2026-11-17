"""Répartition du capital et des droits de vote après l'IPO (prix médian de 74 $, sans greenshoe)."""
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]

ACTIONS_A_TOTAL = 7_427_991_791  # actions A après l'IPO et le placement privé
ACTIONS_N_TOTAL = 5_658_680_800  # actions N après l'IPO et le placement privé
PART_VOIX_ACTION_F = 0.501  # l'action F (Founder LLC) détient 50,1 % des voix, quoi qu'il arrive


def repartition(chemin=RACINE / "data" / "actionnaires.csv"):
    """Tableau par groupe : part du capital et part des droits de vote.

    Les actions N n'ont pas de droit de vote. Les actions A se partagent 49,9 % des voix,
    l'action F (sans droit économique) en détient 50,1 %. La catégorie "autres actionnaires"
    est calculée par différence.
    """
    groupes = pd.read_csv(chemin)
    capital_total = ACTIONS_A_TOTAL + ACTIONS_N_TOTAL
    autres = {
        "groupe": "Autres actionnaires d'avant l'IPO",
        "actions_A": ACTIONS_A_TOTAL - groupes["actions_A"].sum(),
        "actions_N": ACTIONS_N_TOTAL - groupes["actions_N"].sum(),
        "source": "calculé par différence",
    }
    groupes = pd.concat([groupes, pd.DataFrame([autres])], ignore_index=True)
    groupes["part_capital"] = (groupes["actions_A"] + groupes["actions_N"]) / capital_total
    groupes["part_voix"] = groupes["actions_A"] / ACTIONS_A_TOTAL * (1 - PART_VOIX_ACTION_F)

    founder_llc = {
        "groupe": "Founder LLC (action F des 7 cofondateurs)",
        "actions_A": 0,
        "actions_N": 0,
        "source": "S-1/A n°2 Our Governance Structure and Its Goals",
        "part_capital": 0.0,
        "part_voix": PART_VOIX_ACTION_F,
    }
    return pd.concat([groupes, pd.DataFrame([founder_llc])], ignore_index=True)


def voix_des_cofondateurs(tableau):
    """Droits de vote cumulés des 7 cofondateurs : action F plus leurs actions A personnelles."""
    lignes = tableau["groupe"].isin(["7 cofondateurs", "Founder LLC (action F des 7 cofondateurs)"])
    return tableau.loc[lignes, "part_voix"].sum()
