# Prospectus définitif et premier jour de cotation

Sources : prospectus définitif 424B4 du 19/11/2026, S-1/A n°2 du 10/11/2026, cours yfinance (`data/cours_ANT.csv`). Données : `data/ipo_definitive.csv`, `data/premier_jour.csv`.

## 1. Ce qui a changé entre le S-1/A n°2 et le 424B4

| | S-1/A n°2 | 424B4 | Écart |
|---|---|---|---|
| Prix | fourchette 70 à 78 $ (médian 74) | **83 $** | au-dessus de la fourchette |
| Actions A émises par la société | 801 351 354 | 956 351 354 | **+155 000 000** |
| Actions A vendues par des actionnaires | 23 648 646 | 23 648 646 | 0 |
| Total offert | 825 000 000 | 980 000 000 | +155 000 000 |
| Greenshoe | 123 750 000 | 147 000 000 | 15 % du total offert |
| Actions N du placement privé (26 Md$) | 351 351 350 à 74 $ | 313 253 007 | -38 098 343 |
| Produit brut de l'offre | | 81,34 Md$ | |
| Commission des banques | | 550 M$ (0,676 %) | |
| Produit net pour la société, placement compris | | 104,8 Md$ | |

**Lecture.** La demande des investisseurs a été assez forte pour faire les deux à la fois : relever le prix au-delà de la fourchette **et** augmenter le nombre d'actions de 19 %. C'est le signal le plus clair d'un livre d'ordres sursouscrit.

## 2. Pourquoi le nombre total d'actions bouge

Notre modèle (`src/valorisation.py`), construit sur le S-1/A et recalculé à 83 $, donnait une base non diluée de 13 048 574 257 actions. Le 424B4 donne 13 219 642 276. Écart de 171 068 019 actions, entièrement expliqué :

| Explication | Actions |
|---|---|
| Augmentation de l'offre primaire | +155 000 000 |
| Conversion d'actions de préférence (ajustements de dernière minute) | +126 889 (A +112 205, N +14 684) |
| Dette AWS : plus d'actions converties en N à l'IPO, autant de moins en rollover notes | +15 941 130 environ |
| **Total** | **≈ 171 068 019** |

Le point AWS : la dette convertible d'Amazon donne au total 1 840 444 962 actions N. Une partie est convertie à l'IPO, le reste reste sous forme de rollover notes à cause d'un **plafond de détention**. Le plafond étant exprimé en pourcentage du capital, l'augmentation de l'offre l'a fait monter : environ 15,9 millions d'actions passent de « plus tard » à « tout de suite ». Le total ne change pas, donc la base **diluée** n'est pas touchée par ce point.

Base diluée : modèle 17 982 460 989, réel 18 137 587 875, écart 155 126 886, soit l'augmentation de l'offre plus les ajustements de conversion.

## 3. Valorisation au prix final

| À 83 $ | Actions | Capitalisation |
|---|---|---|
| Base non diluée | 13 219 642 276 | 1 097 Md$ |
| Base diluée | 18 137 587 875 | **1 505 Md$** |

## 4. Premier jour (19/11/2026)

| | Valeur |
|---|---|
| Ouverture | 111,50 $ (+34,3 %) |
| Plus haut / plus bas | 115,10 $ / 92,72 $ |
| Clôture | 97,17 $ (**+17,1 %**) |
| Volume | 853 millions d'actions, soit 87 % des actions offertes |
| Capitalisation diluée à la clôture | **1 762 Md$** |

**Argent laissé sur la table** = (clôture moins prix d'IPO) x actions offertes = 14,17 $ x 980 millions = **13,9 Md$**. C'est la valeur que la société et les vendeurs auraient pu capter avec un prix plus proche du cours de marché. S'y ajoutent environ 4,4 Md$ de gain latent pour les partenaires du placement privé, qui ont payé 83 $ eux aussi.

**Lecture du parcours de la journée.** L'ouverture à +34 % puis la clôture à +17 % montrent que les premiers acheteurs ont payé trop cher par rapport à l'équilibre trouvé en fin de séance. Le prix de 83 $ était donc sous-évalué par rapport au marché, mais moins que ne le suggère l'ouverture.

Ordres de grandeur pour comparer : la décote moyenne des IPO américaines au premier jour est d'environ 15 à 20 % sur longue période ; Anthropic est dans cette norme en clôture, au-dessus à l'ouverture.

## 5. Limites

* Un seul jour de cotation : la greenshoe n'est pas encore exercée, et le prix d'équilibre peut encore beaucoup bouger.
* Le volume du premier jour inclut des allers-retours d'investisseurs institutionnels (flipping), il ne mesure pas l'appétit de long terme.
