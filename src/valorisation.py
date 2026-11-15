from donnees import charger_prospectus


def actions_placement_prive(prix, montant):
    """Nombre d'actions N achetées par les partenaires pour un montant fixe en dollars."""
    return montant / prix


def actions_non_diluees(prix, donnees):
    """Nombre total d'actions après l'IPO (sans greenshoe), recalculé pour un prix donné."""
    # a. Actions N qui existaient avant le placement privé (ne dépendent pas du prix)
    actions_N_existantes = (
        donnees["actions_N_apres_ipo_au_prix_median"]
        - donnees["placement_prive_N_actions_au_prix_median"]
    )

    # b. Actions N du placement privé, recalculées au prix demandé
    actions_N_placement = actions_placement_prive(prix, donnees["placement_prive_N_montant"])

    # c. Somme de toutes les classes
    total = (
        donnees["actions_A_apres_ipo"]
        + actions_N_existantes
        + actions_N_placement
        + donnees["actions_T_apres_ipo"]
        + donnees["actions_E_apres_ipo"]
        + donnees["actions_F_apres_ipo"]
    )
    return total


def capitalisation(prix, nb_actions):
    """Capitalisation boursière en dollars."""
    return prix * nb_actions


if __name__ == "__main__":
    donnees = charger_prospectus("data/prospectus.csv")
    for prix in [70, 74, 78]:
        nb_actions = actions_non_diluees(prix, donnees)
        capi = capitalisation(prix, nb_actions)
        print(f"Prix {prix} $ : {nb_actions:,.0f} actions, capitalisation {capi / 1e9:.1f} milliards de dollars")