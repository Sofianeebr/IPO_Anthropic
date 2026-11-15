import pandas as pd


def charger_prospectus(chemin):
    """Lit le fichier du prospectus et renvoie un dictionnaire {indicateur: valeur}."""
    # 1. Lire le CSV avec pandas
    df = pd.read_csv(chemin)
    # 2. Transformer les colonnes "indicateur" et "valeur" en dictionnaire
    dictionnaire = dict(zip(df['indicateur'], df['valeur']))
    # 3. Renvoyer le dictionnaire
    return dictionnaire

if __name__ == "__main__":
    donnees = charger_prospectus("data/prospectus.csv")
    print(donnees)
    print(donnees["prix_median"])