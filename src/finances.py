"""Diagnostic financier d'Anthropic, avec la méthode du cours d'analyse financière (approche Vernimmen).

Montants en millions de dollars, tirés du prospectus S-1/A n°2.
"""
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]


def charger_etats(chemin=RACINE / "data" / "etats_financiers_anthropic.csv"):
    """Tableau poste x période (2023, 2024, 2025, 9M2025, 9M2026)."""
    return pd.read_csv(chemin, index_col="poste").drop(columns=["unite", "source"])


def charger_trimestres(chemin=RACINE / "data" / "trimestres_anthropic.csv"):
    return pd.read_csv(chemin, index_col="poste").drop(columns=["unite", "source"])


def croissance(valeur_fin, valeur_debut):
    """Taux de croissance simple. Attention à l'effet de base quand valeur_debut est petite."""
    return valeur_fin / valeur_debut - 1


def diagnostic(etats):
    """Indicateurs du cours pour chaque période : marges, EBE, CAF, BFR, investissements, flux disponibles."""
    e = etats
    ca = e.loc["chiffre_affaires"]
    ebe = e.loc["resultat_exploitation"] + e.loc["dotations_amortissements"]
    caf = (
        e.loc["resultat_net"]
        + e.loc["remuneration_en_actions"]
        + e.loc["dotations_amortissements"]
        + e.loc["elements_non_monetaires_hors_dotations_et_actions"]
    )
    investissements = -(e.loc["investissements_corporels"] + e.loc["paiements_anticipes_actifs_loues"])
    resultat = pd.DataFrame(
        {
            "chiffre_affaires": ca,
            "marge_exploitation": e.loc["resultat_exploitation"] / ca,
            "marge_exploitation_ajustee": e.loc["resultat_exploitation_ajuste"] / ca,
            "poids_calcul_dans_ca": e.loc["calcul_et_infrastructure"] / ca,
            "marge_apres_calcul": 1 - e.loc["calcul_et_infrastructure"] / ca,
            "ebe": ebe,
            "ebe_hors_remuneration_en_actions": ebe + e.loc["remuneration_en_actions"],
            "caf": caf,
            "variation_bfr": e.loc["variation_bfr"],
            "flux_tresorerie_exploitation": e.loc["flux_tresorerie_exploitation"],
            "investissements": investissements,
            "investissements_sur_dotations": investissements / e.loc["dotations_amortissements"],
            "flux_disponible": e.loc["flux_tresorerie_exploitation"] - investissements,
            "financement_par_actions": e.loc["emission_actions_preference"],
            "financement_par_dette_convertible": e.loc["emission_dette_convertible"],
            "resultat_net": e.loc["resultat_net"],
            "part_juste_valeur_dans_resultat_net": e.loc["variation_juste_valeur_dette_convertible"] / e.loc["resultat_net"],
        }
    )
    return resultat


def chiffre_affaires_annuel(trimestres):
    """Trois mesures du chiffre d'affaires annuel à partir des trimestres."""
    ca = trimestres.loc["chiffre_affaires"]
    return {
        "quatre_derniers_trimestres": ca.iloc[-4:].sum(),
        "dernier_trimestre_annualise": ca.iloc[-1] * 4,
        "croissance_sur_un_an_dernier_trimestre": croissance(ca["T3_2026"], ca["T3_2025"]),
        "croissance_trimestrielle": ca.pct_change().iloc[1:],
    }


def bfr_exploitation(bilan):
    """BFR d'exploitation au 30/09/2026 : créances + charges d'avance moins dettes fournisseurs et produits d'avance."""
    b = bilan
    return (
        b["creances_clients"] + b["charges_constatees_avance_et_autres"]
        - b["dettes_fournisseurs_et_autres"] - b["produits_constates_avance"]
    )


def charger_bilan(chemin=RACINE / "data" / "bilan_anthropic_30_09_2026.csv"):
    return pd.read_csv(chemin, index_col="poste")["valeur"]


if __name__ == "__main__":
    d = diagnostic(charger_etats())
    pd.set_option("display.width", 200)
    print(d.T.round(3))
    print(chiffre_affaires_annuel(charger_trimestres()))
    print("BFR d'exploitation :", bfr_exploitation(charger_bilan()))
