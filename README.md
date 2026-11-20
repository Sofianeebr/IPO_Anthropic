# Analyse de l'IPO d'Anthropic

## Objectifs

Ce projet a pour but de suivre le processus de valorisation durant l'introduction en Bourse (IPO) de l'entreprise Anthropic, et d'analyser sa stratégie concernant les classes d'actions qu'elle émet ainsi que le placement privé réalisé auprès de ses fournisseurs au sein de cette IPO.

### Question centrale

**Combien vaut Anthropic, et le marché a-t-il bien valorisé son introduction en Bourse ?**

1. Que coûte Anthropic au prix de l'IPO ? (valorisation implicite de la fourchette de prix, en base non diluée et diluée)
2. Ce prix est-il justifié ? (comparaison avec des sociétés cotées comparables et valorisation par les flux de trésorerie actualisés)
3. Comment le marché a-t-il réagi ? (rendement du premier jour, volatilité, bêta, fin de la période de blocage)

### Questions d'analyse complémentaires

- Pourquoi tant de classes d'actions ? Quelle est l'utilité de chacune ? (analyse des pondérations, de leurs utilités et des stratégies)
- Pourquoi ce placement privé auprès des fournisseurs ? (comment est-il organisé, quelles sont les stratégies, quels sont les intérêts des fournisseurs)

## Avancement

- [X] Valorisation implicite de la fourchette de prix (base non diluée)
- [X] Valorisation en base totalement diluée
- [X] Analyse des classes d'actions : qui possède et qui décide (`docs/02_gouvernance_et_repartition.md`)
- [X] Analyse du placement privé et du calendrier des ventes futures (`docs/02_gouvernance_et_repartition.md`)
- [X] Diagnostic financier selon la méthode d'analyse financière : croissance, marges, CAF, BFR, investissements, financement (`docs/03_diagnostic_financier.md`)
- [X] Prospectus définitif : écarts avec le S-1/A expliqués, premier jour de cotation (`docs/04_ipo_definitive_et_premier_jour.md`)
- [X] Comparaison avec l'IPO de SpaceX de juin 2026 (`docs/05_comparaison_spacex.md`)
- [X] Dashboard interactif : valorisation, premier jour, diagnostic financier, gouvernance, ventes futures, comparaison avec SpaceX
- [ ] Valorisation par les comparables boursiers et par les flux de trésorerie actualisés
- [ ] Simulation de l'impact des ventes futures, calibrée sur le volume et la volatilité réels de l'action ANT
- [ ] Suivi du cours après le premier jour (volatilité, bêta, fins de lock-up)

## Résultats

### Au prix final (prospectus définitif du 19/11/2026)

| | Anthropic (ANT) | SpaceX (SPCX) |
|---|---|---|
| Prix d'IPO | 83 $ (au-dessus de la fourchette 70 à 78 $) | 135 $ |
| Capitalisation, base non diluée | 1 097 milliards de dollars | 1 776 milliards de dollars |
| Capitalisation, base diluée | 1 505 milliards de dollars | 1 857 milliards de dollars |
| Rendement du premier jour (clôture) | +17,1 % | +19,2 % |
| Argent laissé sur la table | 13,9 milliards de dollars | 16,6 milliards de dollars |
| Capitalisation diluée / CA des 12 derniers mois | environ 43 x | environ 96 x |
| Contrôle des droits de vote | 7 cofondateurs, environ 61 % | Elon Musk, 82,4 % |

L'offre d'Anthropic a été augmentée de 155 millions d'actions entre le S-1/A et le prospectus définitif ; cet écart, plus des ajustements de conversion, explique entièrement la différence entre notre modèle et les chiffres finaux.

### Dans la fourchette du S-1/A n°2

Valorisation implicite de la fourchette de prix (sans greenshoe) :

| Prix par action | Actions, base non diluée | Capitalisation non diluée | Actions, base diluée | Capitalisation diluée |
|---|---|---|---|---|
| 70 $ | environ 13,11 milliards | environ 917 milliards de dollars | environ 18,03 milliards | environ 1 262 milliards de dollars |
| 74 $ | environ 13,09 milliards | environ 968 milliards de dollars | environ 18,01 milliards | environ 1 333 milliards de dollars |
| 78 $ | environ 13,07 milliards | environ 1 019 milliards de dollars | environ 18,00 milliards | environ 1 404 milliards de dollars |

Le nombre d'actions baisse quand le prix monte : les partenaires du placement privé investissent un montant fixe de 26 milliards de dollars, ils reçoivent donc moins d'actions quand chaque action coûte plus cher. En base diluée, la méthode du rachat d'actions joue dans le même sens pour les stock-options.

La base diluée ajoute environ 4,9 milliards d'actions (stock-options, RSU, dette convertible et plans d'abondement des dons des salariés), d'après le tableau de dilution du prospectus. Les calculs retrouvent les totaux du prospectus au prix médian (voir `tests/`).

## Sources

- Prospectus S-1/A n°2 d'Anthropic du 10/11/2026 et prospectus définitif 424B4 du 19/11/2026, déposés auprès de la SEC (EDGAR)
- Prospectus définitif 424B4 de SpaceX du 11/06/2026 et communiqué de clôture du 15/06/2026
- yfinance, pour les cours de ANT et SPCX

## Méthodes utilisées

- Valorisation implicite : prix par action x nombre total d'actions, toutes classes confondues
- Recalcul des actions du placement privé selon le prix (montant fixe de 26 milliards de dollars divisé par le prix)
- Base diluée : méthode du rachat d'actions pour les stock-options (prix d'exercice moyen de 2,91 $), dette convertible incluse, actions T et F sans droit économique exclues
- Diagnostic financier : plan d'analyse financière (croissance et effet de base, marges, CAF, BFR, investissements rapportés aux dotations, flux disponible, structure de financement)
- Premier jour : rendement à l'ouverture et à la clôture, argent laissé sur la table = (clôture moins prix d'IPO) x actions offertes

## Organisation du dossier

| Dossier    | Contenu                                                              |
| ---------- | -------------------------------------------------------------------- |
| `data/`  | données brutes du prospectus, avec leur source                      |
| `docs/`  | notes avec les hypothèses et les analyses                           |
| `src/`   | formules et fonctions pour faire les calculs nécessaires            |
| `tests/` | vérifications des calculs à partir des chiffres du prospectus      |
| `app/`   | dashboard final avec un rendu organisé et synthétique de l'analyse |

## Installation et utilisation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/valorisation.py
python src/finances.py
python src/comparaison.py
pytest
streamlit run app/app.py
```

## Avertissement

Ce projet est purement pédagogique : il n'a en aucun cas pour but de donner un conseil en investissement. Certaines données peuvent être erronées (l'erreur est humaine). N'hésitez pas à signaler tout chiffre incohérent en ouvrant une issue sur ce dépôt.

## Auteur

Sofiane B
