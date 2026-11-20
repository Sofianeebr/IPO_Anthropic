"""Données de marché de l'action ANT après la cotation, et mesures de la réaction du marché."""
from pathlib import Path

import pandas as pd

# Dossier racine du projet, calculé à partir de l'emplacement de ce fichier :
# le code fonctionne quel que soit le dossier depuis lequel on le lance.
RACINE = Path(__file__).resolve().parents[1]
CHEMIN_COURS = RACINE / "data" / "cours_ANT.csv"


def chemin_cours(ticker):
    """Fichier local des cours d'un titre (par exemple data/cours_SPCX.csv)."""
    return RACINE / "data" / f"cours_{ticker}.csv"


def telecharger_cours(ticker="ANT", debut="2026-11-19", chemin=None):
    """Télécharge les cours quotidiens avec yfinance et les enregistre dans un CSV.

    Si le téléchargement échoue (yfinance indisponible, action pas encore cotée),
    on relit la dernière copie enregistrée, pour que les résultats restent reproductibles.
    """
    chemin = chemin or chemin_cours(ticker)
    try:
        import yfinance as yf

        cours = yf.download(ticker, start=debut, auto_adjust=False, progress=False)
        if cours.empty:
            raise ValueError(f"Aucune donnée pour {ticker} depuis le {debut}")
        # yfinance peut renvoyer des colonnes sur deux niveaux (champ, ticker) : on garde le champ
        if isinstance(cours.columns, pd.MultiIndex):
            cours.columns = cours.columns.get_level_values(0)
        cours = cours[["Open", "High", "Low", "Close", "Volume"]]
        cours.to_csv(chemin)
        print(f"{len(cours)} séance(s) téléchargée(s) et enregistrée(s) dans {chemin.name}")
        return cours
    except Exception as erreur:
        print(f"Téléchargement impossible ({erreur}), lecture de la copie locale")
        return charger_cours(chemin)


def charger_cours(chemin=CHEMIN_COURS):
    """Relit les cours enregistrés en local (chemin ou fichier d'un ticker)."""
    return pd.read_csv(chemin, index_col=0, parse_dates=True)


def rendement(prix_depart, prix_arrivee):
    """Rendement simple entre deux prix : (arrivée moins départ) / départ."""
    return (prix_arrivee - prix_depart) / prix_depart


def argent_laisse_sur_la_table(prix_ipo, cours_cloture_jour_1, nb_actions_vendues):
    """Gain des acheteurs de l'IPO dès le premier jour, que la société et les vendeurs n'ont pas encaissé.

    Mesure le coût de la sous-évaluation à l'introduction : (clôture du jour 1 moins prix de l'IPO) x actions vendues.
    """
    return (cours_cloture_jour_1 - prix_ipo) * nb_actions_vendues


def bilan_premier_jour(prix_ipo, cours, nb_actions_vendues=825_000_000):
    """Résumé chiffré du premier jour de cotation."""
    jour_1 = cours.iloc[0]
    return {
        "date": cours.index[0].date(),
        "prix_ipo": prix_ipo,
        "ouverture": jour_1["Open"],
        "cloture": jour_1["Close"],
        "rendement_ouverture": rendement(prix_ipo, jour_1["Open"]),
        "rendement_premier_jour": rendement(prix_ipo, jour_1["Close"]),
        "argent_laisse_sur_la_table": argent_laisse_sur_la_table(prix_ipo, jour_1["Close"], nb_actions_vendues),
        "volume": jour_1["Volume"],
    }


if __name__ == "__main__":
    import sys

    # Utilisation : python src/marche.py PRIX_FINAL_DE_L_IPO
    prix_ipo = float(sys.argv[1]) if len(sys.argv) > 1 else 74.0
    cours = telecharger_cours()
    resultat = bilan_premier_jour(prix_ipo, cours)
    print(f"Premier jour : {resultat['date']}")
    print(f"  Prix de l'IPO : {resultat['prix_ipo']:.2f} $")
    print(f"  Ouverture     : {resultat['ouverture']:.2f} $ ({resultat['rendement_ouverture']:+.1%})")
    print(f"  Clôture       : {resultat['cloture']:.2f} $ ({resultat['rendement_premier_jour']:+.1%})")
    print(f"  Argent laissé sur la table : {resultat['argent_laisse_sur_la_table'] / 1e9:.1f} milliards de dollars")
    print(f"  Volume échangé : {resultat['volume']:,.0f} actions")
