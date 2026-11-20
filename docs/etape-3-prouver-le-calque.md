# Bobinou — Étape 3 : prouver le calque

2026-11-20 · @Nono

Version éditable (commentaires, modifications en ligne) :
https://claude.ai/artifact/FEhb3W8dXdmu2iab2XiwMU

## Objectif

Prouver qu'un calque généré automatiquement est tissable — avant d'écrire la moindre
ligne d'app.

Tout le produit repose dessus : F2 (couleurs) et F3 (matière) travaillent sur les zones
du calque. Si le tracé est trop bruité ou trop simplifié, les deux n'ont plus d'objet.
Le test se fait sans app : un script, une imprimante, l'avis de Justine.

## 1. Ce que Justine doit fournir

C'est le seul vrai délai de l'étape. Deux choses.

**5 à 10 modèles.** Un modèle = l'image que le lissier reproduit en tissage : peinture,
maquette, carton, photo, dessin, motif. Concrètement, des photos prises au téléphone de
ces sources, comme un étudiant les prendrait — un peu de biais, éclairage d'atelier, pas
besoin de belles prises. Avec, pour chacune, les dimensions visées de l'ouvrage en cm.

Faire varier la difficulté :

| Cas | Exemple | Ce qu'il teste |
| --- | --- | --- |
| Dégradés | Paysage, ciel | Le cas dur pour les contours |
| Aplats nets | Motif géométrique, blason | Le témoin facile |
| Zones fines | Visage, main | Là où le calque auto casse |
| Pièce domestique | Assise, tapis | Moins de nuances, autre densité |
| **Calque fait main existant** | Un modèle déjà calqué par Justine | **Comparaison directe : le plus précieux** |

Deux ou trois cas suffisent pour démarrer.

**3 ouvrages déjà réalisés**, avec leur liste de matière réelle : poids par couleur,
fibre, contexture. C'est la seule vérité terrain qui permet de mesurer l'erreur du calcul.

## 2. Le prototype

Un script, pas une app. Démarrable tout de suite sur des peintures du domaine public :
les modèles de Justine servent de validation finale, pas de point de départ.

La chaîne : photo → redressement de perspective → contours à 3 niveaux de détail →
vectorisation → PDF 1:1 paginé A4 avec repères et recouvrement.

Ce qu'il sort, sans aucune vérité terrain :

- nombre et longueur de traits par niveau de détail ;
- nombre de zones fermées, distribution des surfaces en cm² ;
- dérive d'assemblage calculée sur le pavage ;
- réduction de palette à 6 / 12 / 16 tons et surface par ton.

Un emplacement reste vide pour les 3 ouvrages réels : il calculera l'écart entre le poids
prédit et le poids réellement utilisé.

**Analyse de sensibilité — à faire avant l'entretien.** Faire varier consommation,
contexture et marge sur leurs plages plausibles, et mesurer de combien le poids final
bouge. Ça dit quelles réponses de Justine méritent du temps et lesquelles sont du bruit,
donc dans quel ordre poser les questions. Aucune dépendance, une heure de travail.

## 3. Le test papier

Une heure avec Justine, et le point de contrôle qui tranche. Aucune automatisation ne le
remplace : il faut une imprimante, du scotch et un métier.

Imprimer un calque, assembler les pages, le poser sur le métier. Puis trois questions,
rien de plus :

1. Tu peux tisser à partir de ce tracé, oui ou non ?
2. Qu'est-ce que tu dois retoucher, et combien de temps ça te prend ?
3. Les pages s'assemblent droit sur un mètre ?

Noter les réponses telles quelles, y compris ce qui gêne sans être bloquant.

## 4. Verdict

Le livrable de l'étape 3 n'est pas une démo : c'est un tableau de chiffres et un PDF à
scotcher.

| Critère | Mesure | Si ça ne passe pas |
| --- | --- | --- |
| Tracé tissable | Réponse de Justine, oui / non | Revoir l'extraction de contours avant tout développement |
| Retouche raisonnable | Temps de retouche < temps du calque fait main | Renforcer F1 (outils de retouche) ou baisser l'ambition du détail auto |
| Assemblage | Dérive mesurée sur 1 m | Repères et recouvrement à revoir, ou passer au grand format |
| Chiffrage | Écart au poids réel des 3 ouvrages | Corriger la table de consommation avec Justine |

Si les quatre passent, le MVP tient et on enchaîne sur l'étape 4 : choix de la stack (le
prototype dira si le traitement tient sur le téléphone ou demande un serveur), puis F1
dans l'app avec le design déjà fait.

Deux chantiers à mener en parallèle, pas à la place : l'entretien d'une heure avec
Justine, réordonné par l'analyse de sensibilité, et un test des maquettes auprès de 4 à 5
étudiants — le canvas est déjà cliquable, trois écrans réagissent.
