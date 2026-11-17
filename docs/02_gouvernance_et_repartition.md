# Qui possède Anthropic, et qui décide ?

Source : prospectus S-1/A n°2 du 10/11/2026, sections "Our Governance Structure and Its Goals", "Principal and Selling Stockholders", "Risk Factors" et "Shares Eligible for Future Sale". Chiffres après l'IPO et le placement privé, au prix médian de 74 $, sans greenshoe.

## 1. Les trois leviers du pouvoir

| Levier | Qui le détient | Ce qu'il permet |
|---|---|---|
| **Majorité du conseil d'administration** | Long-Term Benefit Trust, via l'unique action T | élire et révoquer la majorité des administrateurs |
| **50,1 % des droits de vote des actionnaires** | Founder LLC (les 7 cofondateurs), via l'unique action F | élire les autres administrateurs, approuver ou bloquer une fusion, une vente de la société, une modification des statuts |
| **Leurs propres actions A** | chaque cofondateur, individuellement | environ 3,2 % des actions A chacun, soit environ 1,6 % des droits de vote chacun |

Les 7 cofondateurs (Dario Amodei, Daniela Amodei, Tom Brown, Jack Clark, Jared Kaplan, Sam McCandlish, Christopher Olah) détiennent donc, ensemble :
* **50,1 % des voix** par l'action F, un pourcentage qui ne baisse pas si la société émet de nouvelles actions
* **environ 11 % des voix supplémentaires** par leurs actions A personnelles (s'ils votaient dans le même sens)
* soit **environ 61 % des droits de vote**, pour **environ 13 % du capital**

Les actions F et T n'ont **aucun droit économique** : elles ne donnent droit ni aux dividendes ni à une part de la valeur de la société. Elles servent uniquement à exercer le pouvoir.

## 2. Propriété du capital et droits de vote : la comparaison

| Actionnaires | Part du capital (économique) | Part des droits de vote | Pouvoir sur le conseil |
|---|---|---|---|
| Nouveaux actionnaires de l'IPO (825 millions d'actions A) | environ 6,3 % | environ 5,5 % | aucun en pratique |
| Amazon (actions N) | environ 14,7 % | 0 % | aucun |
| Google (actions N, placement privé compris) | environ 13,7 % | 0 % | aucun |
| Autres partenaires du placement privé (actions N) | environ 1,7 % | 0 % | aucun |
| Anthropic Public Benefit Fund (actions N) | environ 6,5 % | 0 % | aucun |
| 7 cofondateurs (actions A) | environ 12,8 % | environ 11 % (+ 50,1 % via F) | élisent les administrateurs non désignés par le trust |
| Autres actionnaires d'avant l'IPO (investisseurs privés, salariés) | environ 44 % | environ 33 % | marginal face à l'action F |
| Long-Term Benefit Trust (action T) | 0 % | 0 % sur les votes généraux | **élit la majorité du conseil** |

Calcul : capital économique de 13 086 672 591 actions A et N (hors actions T et F). Droits de vote : l'action F représente 50,1 % du total, les 7 427 991 791 actions A se partagent les 49,9 % restants. Les actions N n'ont pas de droit de vote. La catégorie "autres actionnaires" est calculée par différence.

## 3. Ce qu'on en tire

* **L'IPO ouvre une petite partie du capital au public** : environ 6 % des actions, et environ 5,5 % des droits de vote. Plus de 90 % du capital reste aux actionnaires d'avant l'IPO.
* **Le pouvoir est séparé de la propriété** : les deux leviers décisifs (la majorité du conseil et la majorité des voix) sont attachés à deux actions uniques sans aucune valeur économique. À l'inverse, Amazon et Google, qui détiennent ensemble environ 28 % du capital, n'ont aucun droit de vote.
* **Les grandes décisions dépendent de 7 personnes et d'un trust de 5 membres** : sur une fusion ou une vente, ni le public ni les grands actionnaires économiques ne peuvent imposer une décision.
* Ce schéma est assumé par la société : Anthropic est une **"controlled company"** au sens du Nasdaq, et le prospectus le justifie par la protection de la mission et d'une stratégie de long terme.
* **Point de comparaison** : dans beaucoup d'IPO, les anciens actionnaires gardent aussi la majorité du capital. La particularité d'Anthropic est surtout la **séparation complète entre les droits de vote et la propriété économique**, et un flottant très faible.

## 4. Le risque de ventes futures (overhang)

### Les actions qui pourront arriver sur le marché

Le prospectus détaille le calendrier de fin des périodes de blocage : environ **15,5 milliards d'actions A** pourront être vendues par étapes, à comparer aux **825 millions d'actions** mises en vente lors de l'IPO. Le calendrier complet est dans `data/calendrier_deblocage.csv`. Les étapes les plus importantes :

| Date (estimée) | Actions qui peuvent être vendues |
|---|---|
| premier jour de cotation | jusqu'à 316 millions (salariés et dirigeants hors fondateurs) |
| décembre 2026 à février 2027 | environ 1,3 milliard en quatre étapes |
| 2e jour après les résultats annuels 2026 (estimation : fin février 2027) | jusqu'à 1,7 milliard |
| fin du lock-up de 180 jours (au plus tard le 17/05/2027) | jusqu'à 3,0 milliards |
| fin du lock-up de 365 jours (au plus tard le 18/11/2027) | jusqu'à 1,9 milliard (cofondateurs et actionnaires de plus de 0,5 %) |

### Le cas des actions du placement privé

* Elles ne sont **pas soumises au lock-up**, mais ce sont des **"restricted securities"** : elles ne peuvent être revendues en Bourse qu'après un enregistrement auprès de la SEC ou dans le cadre de la règle 144.
* **Google** dispose de droits d'enregistrement, mais la société n'est pas tenue de déposer publiquement l'enregistrement avant la fin de la "Restricted Period" : le plus tôt entre le 2e jour de Bourse après les résultats du premier trimestre 2027 et le 180e jour après le prospectus. **En pratique, la vente des actions de Google ne semble pas possible avant mai 2027 environ**, soit au même moment que la fin du lock-up de 180 jours.
* **Règle 144** : un actionnaire non affilié peut revendre après 6 mois de détention. Un actionnaire affilié (par exemple un gros actionnaire) est limité, par période de 3 mois, au plus élevé de 1 % des actions A en circulation (environ 74 millions d'actions) ou du volume hebdomadaire moyen des 4 dernières semaines.

### Ce que change une conversion des actions N en actions A

* Une action N se convertit **automatiquement en action A** quand elle est vendue à un tiers non lié.
* **Pas de dilution économique** : aucune action nouvelle n'est créée, la part du capital de chaque actionnaire ne change pas.
* **Dilution des droits de vote** pour les détenteurs d'actions A : de nouvelles actions avec droit de vote apparaissent, alors que l'action F garde 50,1 % des voix.
* **Pression sur le cours** : l'arrivée d'un grand nombre d'actions sur le marché augmente l'offre de titres. L'effet dépend de la taille de la vente rapportée au volume habituellement échangé.

### Comment estimer l'impact d'une vente (méthode prévue pour le dashboard)

1. **Nombre de jours pour écouler la vente** : actions vendues / (volume quotidien moyen x part du volume que le vendeur peut représenter sans trop peser, souvent 10 à 20 %).
2. **Impact estimé sur le prix** (modèle de la "racine carrée", utilisé par les praticiens) : variation de prix d'environ Y x volatilité quotidienne x racine(actions vendues / volume quotidien moyen), avec Y de l'ordre de 0,5 à 1.
3. **Décote d'un bloc** : une vente groupée à des investisseurs (block trade) se fait en général avec une décote par rapport au dernier cours.
4. **Comparaison historique** : les études sur les fins de lock-up observent en moyenne une baisse modérée du cours autour de la date de déblocage, plus marquée quand le volume débloqué est important.

Ces estimations dépendent du volume et de la volatilité observés après la cotation : elles seront calculées à partir des données réelles de l'action ANT.

## 5. Pourquoi ce placement privé auprès des fournisseurs ?

Sources : sections "Concurrent Private Placement" (p. 348), "Liquidity and Capital Resources" (p. 171 à 176), facteurs de risque (p. 77, 78 et 120) et "Shares Eligible for Future Sale" du prospectus.

### Les faits

* Sept entreprises (Google, NVIDIA, AMD, Broadcom, Micron, Microsoft, TSMC) achètent **26 milliards de dollars d'actions N** (sans droit de vote) au prix de l'IPO. Chacune s'engage séparément.
* **Aucune commission** n'est versée aux banques sur ce montant. Le placement dépend de la réalisation de l'IPO, mais l'IPO ne dépend pas du placement.
* Les actions ne sont **pas soumises au lock-up**, mais ce sont des titres restreints : leur revente en Bourse suppose un enregistrement auprès de la SEC ou le respect de la règle 144.
* Le placement s'inscrit dans des **accords industriels plus larges** :
  * **Google** (10 milliards) exerce une option accordée dans le cadre d'un financement de 20 milliards de dollars signé en 2026, dont les tirages sont liés aux accords d'achat de puissance de calcul d'Anthropic et à des objectifs de chiffre d'affaires. Sa participation est plafonnée à 14,99 % du capital.
  * **AMD** (2,5 milliards) verse une partie d'un engagement de 5 milliards prévu par un contrat de fourniture de GPU. Le solde sera versé au rythme des livraisons de GPU, à partir de 2027, au cours moyen de l'action.
* Amazon, Google et Microsoft sont à la fois **actionnaires, fournisseurs de puissance de calcul, distributeurs, clients et concurrents** d'Anthropic. Le prospectus reconnaît que cette situation crée des conflits d'intérêts et une dépendance.

### L'intérêt d'Anthropic

* **Lever des capitaux sans commission** : 26 milliards de dollars, soit environ 30 % du montant brut levé au total (environ 85 milliards).
* **Sécuriser sa puissance de calcul**, sa ressource la plus critique, en liant ses fournisseurs à sa réussite.
* **Envoyer un signal au marché** : les plus grandes entreprises du secteur investissent au même prix que le public.
* **Connaître le montant levé à l'avance** : le placement est fixé en dollars, quel que soit le prix final.

### L'intérêt des partenaires

* **Une exposition économique à la croissance d'Anthropic sans droit de vote** : les actions N évitent d'apparaître comme cherchant à contrôler un client ou un concurrent, un point sensible au regard du droit de la concurrence.
* **La sécurisation d'un très gros client** : Anthropic achète de la puissance de calcul, des puces et de la mémoire à la plupart de ces entreprises.
* **Une certaine liquidité** : pas de lock-up, même si la revente reste encadrée (pour Google, pas avant mai 2027 environ).

### Une relation circulaire

L'accord d'AMD illustre le mécanisme : AMD investit dans Anthropic au rythme des GPU qu'Anthropic lui achète. Une partie de l'argent investi revient donc au fournisseur sous forme de ventes. C'est un **financement fournisseur** : AMD aide son client à financer ses achats et prend en contrepartie un risque sur la valeur des actions. Ce n'est pas une remise directe, puisque les actions sont achetées au prix du marché.

### Ce que ça implique pour un actionnaire A

* **Dépendance** : l'activité d'Anthropic repose sur un petit nombre de fournisseurs qui sont aussi des concurrents.
* **Pression vendeuse future** : les actions N des partenaires, d'Amazon et de Google se convertissent en actions A en cas de vente à un tiers. Une vente importante augmenterait l'offre de titres sur le marché, en particulier autour de mai 2027, quand se cumulent la fin du lock-up de 180 jours et la possibilité d'enregistrement pour Google.
* **Pas de dilution économique** lors d'une conversion, mais une **dilution des droits de vote** des détenteurs d'actions A.

### Synthèse

Le placement privé est moins un investissement financier qu'un **élément d'accords industriels** entre Anthropic et ses fournisseurs : il apporte du capital et sécurise l'approvisionnement en puissance de calcul, au prix d'une dépendance accrue et de relations d'affaires croisées.
