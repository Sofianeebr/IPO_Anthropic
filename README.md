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
- [ ] Analyse des classes d'actions et du placement privé
- [ ] Valorisation par les comparables et par les flux de trésorerie actualisés
- [ ] Réaction du marché après la cotation
- [ ] Dashboard interactif

## Premiers résultats

Valorisation implicite de la fourchette de prix (sans greenshoe) :

| Prix par action | Actions, base non diluée | Capitalisation non diluée | Actions, base diluée | Capitalisation diluée |
|---|---|---|---|---|
| 70 $ | environ 13,11 milliards | environ 917 milliards de dollars | environ 18,03 milliards | environ 1 262 milliards de dollars |
| 74 $ | environ 13,09 milliards | environ 968 milliards de dollars | environ 18,01 milliards | environ 1 333 milliards de dollars |
| 78 $ | environ 13,07 milliards | environ 1 019 milliards de dollars | environ 18,00 milliards | environ 1 404 milliards de dollars |

Le nombre d'actions baisse quand le prix monte : les partenaires du placement privé investissent un montant fixe de 26 milliards de dollars, ils reçoivent donc moins d'actions quand chaque action coûte plus cher. En base diluée, la méthode du rachat d'actions joue dans le même sens pour les stock-options.

La base diluée ajoute environ 4,9 milliards d'actions (stock-options, RSU, dette convertible et plans d'abondement des dons des salariés), d'après le tableau de dilution du prospectus. Les calculs retrouvent les totaux du prospectus au prix médian (voir `tests/`).

## Sources

- Prospectus S-1/A d'Anthropic du 10/11/2026, déposé auprès de la SEC (EDGAR)
- yfinance, pour les données de marché après la cotation

## Méthodes utilisées

- Valorisation implicite : prix par action x nombre total d'actions, toutes classes confondues
- Recalcul des actions du placement privé selon le prix (montant fixe de 26 milliards de dollars divisé par le prix)
- Base diluée : méthode du rachat d'actions pour les stock-options (prix d'exercice moyen de 2,91 $), dette convertible incluse, actions T et F sans droit économique exclues

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
pytest
```

## Avertissement

Ce projet est purement pédagogique : il n'a en aucun cas pour but de donner un conseil en investissement. Certaines données peuvent être erronées (l'erreur est humaine). N'hésitez pas à signaler tout chiffre incohérent en ouvrant une issue sur ce dépôt.

## Auteur

Sofiane B
