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


def actions_rachetees_options(prix, donnees):
    """Méthode du rachat d'actions : actions rachetées avec l'argent payé par les salariés pour exercer leurs options."""
    argent_des_options = donnees["dil_options_brutes"] * donnees["exclu_options_prix_exercice_moyen"]
    return argent_des_options / prix


def actions_diluees(prix, donnees):
    """Nombre total d'actions en base totalement diluée, recalculé pour un prix donné.

    Reprend le tableau de dilution de la page 24 du prospectus (S-1/A n°2).
    Hypothèses : les 2 actions T et F (sans droit économique) sont exclues,
    les rollover notes de la dette convertible sont incluses.
    """
    # a. Ce qui ne dépend pas du prix
    actions_A = donnees["dil_actions_A_total"]
    actions_N_sans_placement = (
        donnees["dil_actions_N_total_au_prix_median"]
        - donnees["placement_prive_N_actions_au_prix_median"]
    )
    options_brutes = donnees["dil_options_brutes"]
    rsu = donnees["dil_rsu_total"]

    # b. Ce qui dépend du prix
    actions_N_placement = actions_placement_prive(prix, donnees["placement_prive_N_montant"])
    options_rachetees = actions_rachetees_options(prix, donnees)

    # c. Total
    total = (
        actions_A
        + actions_N_sans_placement
        + actions_N_placement
        + options_brutes
        - options_rachetees
        + rsu
    )
    return total


def capitalisation(prix, nb_actions):
    """Capitalisation boursière en dollars."""
    return prix * nb_actions


if __name__ == "__main__":
    donnees = charger_prospectus("data/prospectus.csv")
    for prix in [70, 74, 78]:
        nb_non_dilue = actions_non_diluees(prix, donnees)
        nb_dilue = actions_diluees(prix, donnees)
        capi_non_diluee = capitalisation(prix, nb_non_dilue)
        capi_diluee = capitalisation(prix, nb_dilue)
        print(f"Prix {prix} $")
        print(f"  Base non diluée : {nb_non_dilue:,.0f} actions, capitalisation {capi_non_diluee / 1e9:.1f} milliards de dollars")
        print(f"  Base diluée     : {nb_dilue:,.0f} actions, capitalisation {capi_diluee / 1e9:.1f} milliards de dollars")
