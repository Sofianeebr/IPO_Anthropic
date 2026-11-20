# Diagnostic financier d'Anthropic

Source : prospectus S-1/A n°2 (états financiers consolidés, MD&A, résultats trimestriels). Montants en millions de dollars. Exercices clos le 31 décembre ; 9M = neuf mois clos le 30 septembre. Code : `src/finances.py`, données : `data/etats_financiers_anthropic.csv`, `data/trimestres_anthropic.csv`, `data/bilan_anthropic_30_09_2026.csv`.

La méthode suit le plan classique de l'analyse financière (approche Vernimmen) : création de valeur par l'activité (croissance, marges), puis politique d'investissement (BFR, immobilisations), puis financement, puis rentabilité et risque.

## 1. Croissance du chiffre d'affaires

| | 2023 | 2024 | 2025 | 9M2025 | 9M2026 |
|---|---|---|---|---|---|
| Chiffre d'affaires | 41 | 386 | 4 585 | 2 545 | 33 242 |
| Croissance | | x 9,4 | x 11,9 | | x 13,1 |

**Effet de base.** Des multiplications par 9 ou 12 sont possibles parce que le point de départ est minuscule (41 M$ en 2023). Ce rythme ne se prolonge pas mécaniquement : passer de 35 Md$ à 420 Md$ en un an demanderait des clients qui n'existent pas encore.

Le rythme trimestriel le montre déjà :

| Trimestre | T1 25 | T2 25 | T3 25 | T4 25 | T1 26 | T2 26 | T3 26 |
|---|---|---|---|---|---|---|---|
| CA | 376 | 787 | 1 382 | 2 040 | 4 731 | 11 555 | 16 956 |
| Croissance sur le trimestre précédent | | +109 % | +76 % | +48 % | +132 % | +144 % | +47 % |

Le T3 2026 reste en croissance de 1 127 % sur un an, mais la croissance d'un trimestre sur l'autre est retombée à +47 %.

**Trois mesures du chiffre d'affaires annuel**, utiles pour les multiples :
* 12 derniers mois (T4 25 à T3 26) : **35,3 Md$**
* dernier trimestre x 4 : **67,8 Md$**
* revenu annualisé déclaré par la société au 31/10/2026 (run-rate) : **81 Md$**

Le choix de la mesure change le multiple d'un facteur 2,3. C'est le premier point à vérifier quand on lit qu'Anthropic « vaut X fois son chiffre d'affaires ».

## 2. Marges et structure de coûts

| | 2023 | 2024 | 2025 | 9M2025 | 9M2026 |
|---|---|---|---|---|---|
| Calcul et infrastructure / CA | 1 056 % | 653 % | 160 % | 172 % | 56,6 % |
| Marge après calcul | négative | négative | négative | négative | 43,4 % |
| Marge d'exploitation | négative | négative | -176 % | -205 % | -3,8 % |
| Marge d'exploitation ajustée (hors rémunération en actions) | négative | négative | -106 % | -123 % | +12,3 % |

* Le coût du calcul (location de GPU et de centres de données) est le principal coût variable. Il passe de 10 fois le chiffre d'affaires en 2023 à 57 % en 2026 : chaque dollar vendu coûte de moins en moins de calcul.
* Le reste (recherche, salaires, commercial) est plus proche d'un coût fixe : il grandit moins vite que le CA, d'où le levier opérationnel.
* Au T2 2026 le résultat d'exploitation est positif (+974 M$), puis redevient négatif au T3 (-567 M$) car le calcul progresse plus vite que le CA ce trimestre (x 1,77 contre x 1,47).

## 3. Du résultat net à la trésorerie

Le résultat net des 9M2026 est de **-104 Md$**, mais il n'a presque rien à voir avec l'activité :

| 9M2026 | M$ |
|---|---|
| Résultat d'exploitation | -1 260 |
| Variation de juste valeur de la dette convertible | -94 324 |
| Autres éléments financiers | environ -10 300 |
| Résultat net | -104 039 |

La dette convertible est comptabilisée à sa juste valeur. Quand la valeur d'Anthropic monte, la valeur des actions promises aux prêteurs monte aussi, et cette hausse est enregistrée comme une charge. **Plus la société vaut cher, plus sa perte comptable est grande.** C'est une charge non monétaire : aucun dollar ne sort. Elle disparaît à l'IPO, quand la dette est convertie en actions.

**CAF, BFR, flux d'exploitation (9M2026) :**

| | M$ |
|---|---|
| Résultat net | -104 039 |
| + rémunération en actions | +3 255 |
| + dotations aux amortissements | +250 |
| + autres éléments non monétaires (juste valeur surtout) | +106 676 |
| **= CAF** | **6 142** |
| Variation de BFR (signe du tableau de flux) | +427 |
| **= Flux de trésorerie d'exploitation** | **6 569** |

L'activité génère donc de la trésorerie sur 2026, alors que le compte de résultat affiche une perte record.

## 4. Investissements

| 9M2026 | M$ |
|---|---|
| Acquisitions d'immobilisations corporelles | 925 |
| Paiements d'avance sur actifs loués (centres de données) | 1 955 |
| Total investissements | 2 880 |
| Dotations aux amortissements | 250 |
| **Investissements / dotations** | **11,5** |

Un ratio très supérieur à 1 signifie que la société construit son outil de production bien plus vite qu'il ne s'use. Mais l'essentiel de la capacité de calcul est **loué** et non possédé : le vrai engagement est hors bilan, sous forme de **900,9 Md$ d'engagements d'achat de calcul**, dont 70,7 Md$ à moins d'un an. C'est 11 fois le run-rate de 81 Md$.

**Flux de trésorerie disponible (9M2026)** = 6 569 moins 2 880 = **environ +3,7 Md$**.

## 5. BFR et bilan au 30/09/2026

| Actif économique | M$ | Financement | M$ |
|---|---|---|---|
| Immobilisations corporelles | 3 061 | Capitaux propres (avant IPO) | -149 873 |
| Droits d'utilisation | 2 839 | Actions de préférence remboursables | 157 510 |
| Goodwill et autres actifs non courants | 4 860 | Dette convertible (juste valeur) | 130 502 |
| BFR d'exploitation | -2 222 | Dettes de location | 2 810 |
| | | moins trésorerie et placements | -131 845 |

* **BFR d'exploitation négatif** (créances 7 892 + charges d'avance 1 283, moins fournisseurs 9 426 et produits constatés d'avance 1 971) : les clients et fournisseurs financent l'exploitation. Délai clients d'environ 42 jours de CA.
* **Capitaux propres négatifs** avant IPO : effet comptable des actions de préférence classées hors capitaux propres et des pertes de juste valeur. Après conversion à l'IPO, les capitaux propres pro forma deviennent positifs (23 449 M$ au prix médian).
* **Financement** : 110,4 Md$ levés en actions de préférence sur 9M2026, plus l'IPO et le placement privé (104,8 Md$ net). La dette financière nette est fortement négative (trésorerie supérieure aux dettes) : le ratio **DFN / EBE n'a pas de sens** ici.

## 6. Ce qu'on en retient pour la valorisation

* La croissance est réelle et documentée, mais en décélération trimestrielle.
* La marge après calcul s'améliore vite : c'est elle qui justifie, ou non, une valorisation élevée.
* La perte nette est trompeuse ; il faut lire le résultat d'exploitation et les flux de trésorerie.
* Le principal risque financier est hors bilan : les 900,9 Md$ d'engagements de calcul supposent que le CA continue de croître.

| Multiple (prix d'IPO 83 $, base diluée, capitalisation 1 505 Md$) | Valeur |
|---|---|
| sur CA des 12 derniers mois (35,3 Md$) | environ 43 x |
| sur CA du T3 annualisé (67,8 Md$) | environ 22 x |
| sur run-rate (81 Md$) | environ 19 x |
