# Étape 3 — analyse de sensibilité du chiffrage

2026-11-24. Script : [`prototype/sensibilite.py`](../prototype/sensibilite.py),
200 000 tirages, cas de référence 60 × 100 cm (0,60 m²).

L'étape 3 prévoyait cette analyse « avant l'entretien », pour savoir quelles réponses
de Ju méritent du temps. Elle répond à ça, et à une question qu'on n'avait pas posée
et qui est meilleure.

## Ce qui pèse sur le poids annoncé

Poids nominal, consommation 1,5 kg/m² et marge 15 % : **1,30 kg**.

| Variable | Plage | Poids | Amplitude |
| --- | --- | --- | --- |
| **Consommation** | 1 – 2 kg/m² | 0,95 – 1,64 kg | **53 %** |
| Cote largeur | 55 – 65 cm | 1,20 – 1,40 kg | 16 % |
| Cote hauteur | 92 – 108 cm | 1,20 – 1,40 kg | 15 % |
| Marge de perte | 5 – 25 % | 1,21 – 1,39 kg | 14 % |
| Contexture (rang entier) | 2,2 – 5,6 fils/cm | 1,29 – 1,41 kg | 9 % |
| Longueur de montage | 0,30 – 0,60 m | 1,27 – 1,33 kg | 4 % |

Tout à la fois : P5 0,99 · médiane 1,33 · P95 1,72 kg, soit une fourchette de **×1,74**.

Part de variance (R² du modèle linéaire : 0,965, donc le modèle est assez linéaire
pour qu'on lise ces parts) :

| | |
| --- | --- |
| Consommation | **79,7 %** |
| Cote largeur | 7,6 % |
| Cote hauteur | 6,6 % |
| Marge de perte | 5,4 % |
| Longueur de montage | 0,7 % |
| Contexture | **0,0 %** |

La prédiction faite hier se confirme : la consommation écrase tout. Quatre cinquièmes
de l'incertitude tiennent dans une seule inconnue.

## Deux surprises

**La contexture ne compte pour rien.** Pas parce qu'elle serait négligeable, mais
parce que les deux effets s'annulent. Dans la table de Galice p. 22, le métrage au
kilo et le nombre de fils au centimètre montent ensemble : une chaîne plus fine, c'est
plus de fils, mais un fil plus léger. 2,2 fils/cm à 750 m/kg pèsent 0,26 kg,
5,6 fils/cm à 1 650 m/kg en pèsent 0,30. La chaîne reste entre **0,18 et 0,48 kg**
quoi qu'on fasse.

C'est un piège de modélisation évité de peu : en faisant varier les fils/cm seuls, à
métrage fixé, on obtenait 30 % d'amplitude — un artefact, puisque cette combinaison
n'existe pas dans la table. **Il faut tirer un rang entier, pas deux valeurs
indépendantes.** Conséquence directe pour l'app : le curseur de contexture de l'écran
`Chiffrage` ne doit pas être libre, il doit proposer les rangs de la table.

**La chaîne pèse 23 % du total** et presque rien en incertitude. Elle mérite donc
d'être comptée à part — ce que les maquettes font déjà — mais elle ne mérite aucune
question à Ju.

## La meilleure question : la marge couvre-t-elle l'erreur ?

Se tromper de 20 % par excès coûte un peu de laine. De 20 % par défaut, ça coûte un
bain de teinture et une rupture de ton au milieu de la pièce — c'est précisément ce
contre quoi Galice met en garde (p. 61).

On sépare donc ce que l'app **croit** de ce qui **est**, et on compte la proportion de
cas où la prédiction passe sous le besoin réel.

Marge nécessaire pour descendre sous **5 % de risque de manquer** :

| Scénario | Marge |
| --- | --- |
| Cotes déduites, pas d'essai pesé | **35 %** |
| Cotes relevées au mètre, pas d'essai | **30 %** |
| Cotes déduites, essai de 10 × 10 pesé | **15 %** |
| Cotes relevées **et** essai pesé | **5 %** |

Lecture : sans essai pesé, il faut prévoir un tiers de laine en plus pour être
tranquille, et relever les cotes au mètre ne fait gagner que 5 points. **L'essai pesé
en fait gagner 20.** Les deux ensemble ramènent la marge de 35 % à 5 %.

À marge nulle, le risque est de 50 % dans tous les cas — c'est le contrôle de
cohérence : une prédiction centrée se trompe par défaut une fois sur deux.

## Ce que ça décide

**1. L'écran `Chiffrage` a besoin du champ « j'ai pesé mon essai ».** Ce n'était
jusqu'ici qu'une bonne idée tirée du livre et du référentiel BMA. C'est maintenant la
seule mesure qui change quelque chose, et on sait de combien : 20 points de marge.
Sans elle, l'app annonce une quantité dont elle sait qu'elle est fausse d'un facteur
proche de 2.

**2. La marge par défaut ne peut pas être une constante.** Elle doit dépendre de ce
que l'étudiant a fourni : 35 % s'il n'a rien mesuré, 5 % s'il a pesé son essai et
relevé ses cotes. Une marge fixe à 10 % donnerait un tiers de chances de manquer.

**3. L'ordre des questions à Ju est fixé** — et l'entretien se raccourcit :

| Rang | Question | Pourquoi |
| --- | --- | --- |
| 1 | **Ta consommation réelle, en kg/m², sur des ouvrages que tu as pesés** | 80 % de l'incertitude |
| 2 | Les **cotes exactes** des pièces photographiées | 14 % à elles deux |
| 3 | Quelle **marge** tu prends, et si tu as déjà manqué | 5 %, mais c'est le réglage par défaut de l'app |
| — | ~~Contexture~~ | 0 %. Utile pour le rendu, inutile pour le poids |
| — | ~~Longueur de montage~~ | 0,7 % |

Les deux dernières lignes sont le vrai gain de cette analyse : **deux questions en
moins**, et la certitude qu'on ne perd rien à les supprimer.

## Limites

- La consommation est tirée uniformément entre 1 et 2 kg/m². C'est la plage du livre,
  pas une distribution observée ; si la pratique se concentre autour de 1,3, tous les
  risques baissent. Les **3 ouvrages réels** trancheront.

  *Vérifié le 2026-11-24 : aucune source publique ne donne de consommation au m² pour
  la tapisserie de lisse — les ateliers décrivent le kilotage sans jamais en publier le
  ratio (voir [`reponses-metier.md`](./reponses-metier.md) § 9). La plage de Galice
  reste la seule référence. Attention au chiffre de 1,2 kg/m² qui circule : il concerne
  la tapisserie **au petit point**, de la broderie sur canevas, pas du tissage.*
- Le modèle ignore la répartition par couleur. Manquer de 10 % sur le ton dominant
  n'a pas le même coût que sur un ton qui couvre 2 % de la surface. À reprendre quand
  F2 sortira les surfaces par ton — le prototype les calcule déjà.
- La soie et le coton ne sont pas modélisés : tout est en laine, comme aux Gobelins.
