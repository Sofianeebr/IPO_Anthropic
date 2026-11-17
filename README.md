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

Valorisation implicite de la fourchette de prix, en base non diluée (sans greenshoe) :

| Prix par action | Nombre d'actions        | Capitalisation                     | Base non diluée                                       | Base diluée                                |
| --------------- | ----------------------- | ---------------------------------- | ------------------------------------------------------ | ------------------------------------------- |
| 70 $            | environ 13,11 milliards | environ 917 milliards de dollars   | capitalisation 917.5 milliards de dollars         | 1262.0 milliards de dollars                 |
| 74 $            | environ 13,09 milliards | environ 968 milliards de dollars   | capitalisation 968.4 milliards de dollars              | capitalisation 1333.0 milliards de dollars  |
| 78 $            | environ 13,07 milliards | environ 1 019 milliards de dollars | capitalisation 1019.4 milliards de dollars             | capitalisation 1403.9 milliards de dollars  |

Le nombre d'actions baisse quand le prix monte : les partenaires du placement privé investissent un montant fixe de 26 milliards de dollars, ils reçoivent donc moins d'actions quand chaque action coûte plus cher.

## Sources

- Prospectus S-1/A d'Anthropic du 10/11/2026, déposé auprès de la SEC (EDGAR)
- yfinance, pour les données de marché après la cotation

## Méthodes utilisées

- Valorisation implicite : prix par action x nombre total d'actions, toutes classes confondues
- Recalcul des actions du placement privé selon le prix (montant fixe de 26 milliards de dollars divisé par le prix)

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
```

## Avertissement

Ce projet est purement pédagogique : il n'a en aucun cas pour but de donner un conseil en investissement. Certaines données peuvent être erronées (l'erreur est humaine). N'hésitez pas à signaler tout chiffre incohérent en ouvrant une issue sur ce dépôt.

## Auteur

Sofiane B
