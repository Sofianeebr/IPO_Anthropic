# Comparaison avec l'IPO de SpaceX

Sources : prospectus définitif 424B4 de SpaceX du 11/06/2026, communiqué de clôture du 15/06/2026, cours yfinance (`data/cours_SPCX.csv`). Données : `data/spacex.csv`. Code : `src/comparaison.py`.

SpaceX (Nasdaq : SPCX) est entrée en Bourse le 12/06/2026, cinq mois avant Anthropic. Les deux opérations sont les plus grosses IPO de l'histoire et partagent un trait commun : des fondateurs qui gardent le contrôle avec une petite part du capital.

## 1. L'offre

| | Anthropic | SpaceX |
|---|---|---|
| Prix d'IPO | 83 $ | 135 $ |
| Actions offertes (hors greenshoe) | 980 000 000 | 555 555 555 |
| dont vendues par des actionnaires | 23 648 646 | 0 |
| Greenshoe | 147 000 000 (non encore exercée) | 83 333 333 (exercée en totalité) |
| Produit brut de l'offre | 81,3 Md$ | 75,0 Md$ |
| Placement privé simultané | 26 Md$ (fournisseurs de calcul) | aucun |
| Commission des banques | 0,676 % | 0,667 % |

Les deux commissions sont très basses par rapport à la norme américaine (environ 4 à 7 % pour une IPO moyenne) : sur des opérations de cette taille, les banques acceptent un pourcentage faible pour un montant absolu élevé et pour le prestige.

## 2. Valorisation à l'IPO

| | Anthropic | SpaceX |
|---|---|---|
| Actions, base non diluée | 13,22 Md | 13,16 Md |
| Actions, base diluée | 18,14 Md | 13,76 Md |
| Capitalisation non diluée | 1 097 Md$ | 1 776 Md$ |
| Capitalisation diluée | 1 505 Md$ | 1 857 Md$ |
| Écart dilué / non dilué | +37 % | +5 % |

Pour SpaceX, la base diluée est calculée avec la méthode du rachat d'actions : les options A (prix d'exercice moyen 27,65 $) et B (8,22 $) sont dans la monnaie à 135 $, l'argent de leur exercice rachète une partie des actions.

**L'écart de dilution est très différent.** Chez Anthropic, il vient surtout des rollover notes d'Amazon et des options et RSU des salariés, nombreuses dans une société jeune qui paie en actions. Chez SpaceX, la société est plus ancienne et les instruments dilutifs sont peu nombreux par rapport au capital.

## 3. Qui décide ?

| | Anthropic | SpaceX |
|---|---|---|
| Mécanisme de contrôle | action F (50,1 % des voix fixes) + action T (majorité du conseil élue par le trust) | actions B à 10 voix |
| Contrôle | 7 cofondateurs : environ 61 % des voix | Elon Musk seul : 82,4 % des voix |
| Part du capital correspondante | environ 13 % | environ 46 % (estimation) |
| Flottant (actions offertes / base) | 7,4 % | 4,9 % |

L'estimation pour Musk part des parts de voix du prospectus : 81,1 % des voix via les actions B, à 10 voix chacune, donne environ 5,2 Md d'actions B ; les 1,3 % restants via des actions A donnent environ 0,8 Md d'actions A.

**Différence de nature.** Chez SpaceX, le contrôle reste lié à la propriété : les actions B ont aussi des droits économiques, et Musk possède près de la moitié de la société. Chez Anthropic, le pouvoir est séparé de la propriété : les actions F et T n'ont aucune valeur économique, et la mission (PBC, Long-Term Benefit Trust) est le motif affiché de cette séparation.

## 4. Fondamentaux

| | Anthropic | SpaceX |
|---|---|---|
| CA des 12 derniers mois | 35,3 Md$ | 19,3 Md$ |
| Croissance sur un an (dernier trimestre) | +1 127 % | +15,4 % |
| Marge d'exploitation (dernière période) | -3,8 % (9M2026) | -41 % (T1 2026), -13,9 % (2025) |
| Flux d'exploitation 2025 | -2,6 Md$ | +6,8 Md$ |
| Investissements 2025 | 0,2 Md$ en propre, plus engagements de calcul loués | 20,7 Md$ (111 % du CA) |
| Flux disponible 2025 | environ -2,8 Md$ | environ -14,0 Md$ |
| **Capitalisation diluée / CA 12 mois** | **43 x** | **96 x** |

**Deux modèles d'investissement opposés.** SpaceX possède ses actifs (fusées, satellites Starlink) et les finance au bilan, d'où des investissements supérieurs au CA. Anthropic loue sa capacité de calcul : ses investissements au bilan sont faibles, mais ses engagements hors bilan (900,9 Md$) sont énormes. Les deux sociétés brûlent du capital pour construire de la capacité, simplement à des endroits différents des états financiers.

**Le multiple.** SpaceX a été introduite à un multiple de CA plus de deux fois supérieur à celui d'Anthropic, pour une croissance bien plus faible. Le marché paie donc chez SpaceX autre chose que la croissance actuelle : la position quasi monopolistique dans le lancement spatial, la base d'abonnés Starlink et des options sur des marchés futurs. Chez Anthropic, il paie surtout la vitesse de croissance.

## 5. Premier jour et parcours en Bourse

| | Anthropic (19/11/2026) | SpaceX (12/06/2026) |
|---|---|---|
| Rendement à l'ouverture | +34,3 % | +11,1 % |
| Rendement à la clôture | +17,1 % | +19,2 % |
| Volume / actions offertes | 87 % | 81 % |
| Argent laissé sur la table | 13,9 Md$ | 16,6 Md$ (greenshoe comprise) |
| Capitalisation diluée à la clôture | 1 762 Md$ | 2 214 Md$ |

Profils opposés sur la journée : Anthropic ouvre très haut puis redescend, SpaceX ouvre modestement puis monte.

Parcours de SpaceX depuis son IPO : plus haut de clôture 211,39 $ le 16/06/2026 (+57 % sur le prix d'IPO), plus bas 108,27 $ le 05/08/2026 (-20 %), clôture 138,43 $ le 19/11/2026 (+2,5 %). Cinq mois après, l'action est revenue près de son prix d'introduction après un fort aller-retour. C'est un rappel que le premier jour dit peu de chose de la valeur à moyen terme, et que les fins de lock-up pèsent sur le cours.

## 6. Ce qu'on en retient

* Les deux IPO ont été « réussies » au sens du premier jour, avec une décote dans la norme historique.
* Anthropic est moins chère que SpaceX en multiple de CA, mais son CA est plus récent et dépend d'engagements de calcul massifs.
* Les deux structures de gouvernance laissent le public sans pouvoir réel ; celle d'Anthropic va plus loin en séparant entièrement pouvoir et propriété.
* Le parcours de SpaceX donne un scénario de référence pour les mois à venir chez Anthropic : volatilité forte et pression des déblocages de lock-up.
