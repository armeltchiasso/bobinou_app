# Bobinou — Étape 3 : prouver le calque

2026-11-20 · @Nono · **révisé le 2026-11-23**

Version éditable (commentaires, modifications en ligne) :
https://claude.ai/artifact/FEhb3W8dXdmu2iab2XiwMU

> **Révision du 2026-11-23.** Les réponses métier
> ([`reponses-metier.md`](./reponses-metier.md)) ont corrigé trois hypothèses de ce plan :
> le calque s'emploie **à l'envers**, il se fragmente en **bandes de 20 ou 40 cm de haut**
> au lieu d'un pavage A4 libre, et le critère « temps du calque fait main » ne vaut que
> mesuré sur un cas précis — l'ordre de grandeur publié, de **quelques heures à plusieurs
> jours**, est trop large pour servir de seuil. Les sections 2, 3 et 4 ont été reprises.

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
besoin de belles prises. Avec, pour chacune, **les dimensions visées de l'ouvrage en cm**
et **la technique** (haute lice, basse lice, Savonnerie) : elle fixe le sens du calque et
le pas des bandes.

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
vectorisation → **miroir horizontal** → PDF 1:1 **découpé en bandes**, avec ligne de
cordeau, repères latéraux et recouvrement.

Deux points de sortie sont imposés par le métier, pas par le confort d'impression
(Galice, p. 65, 69 et 179 — détail dans [`reponses-metier.md`](./reponses-metier.md)) :

- **Miroir.** En haute lice le calque est vu à contre-jour depuis l'arrière du métier,
  donc inversé ; en basse lice il est explicitement « repris à l'envers » sur papier
  toilé. Un calque en lecture directe est inutilisable dans les deux cas.
- **Bandes horizontales de 20 cm** (motifs détaillés) ou **40 cm** (motifs larges), pas
  un pavage libre. Au-delà, les fils de chaîne travaillent et un trait horizontal devient
  une dent de scie. Chaque bande porte en pleine largeur la **ligne de cordeau** qui sert
  de repère maître, et chevauche la partie déjà tissée. Le pas se déduit du niveau de
  détail : c'est le même curseur.

Ce qu'il sort, sans aucune vérité terrain :

- nombre et longueur de traits par niveau de détail ;
- nombre de zones fermées, distribution des surfaces en cm² ;
- nombre de bandes et pas retenu, largeur de recouvrement, écart de raccord au cordeau
  d'une bande à la suivante ;
- réduction de palette à 6 / 12 / 16 tons et surface par ton.

Un emplacement reste vide pour les 3 ouvrages réels : il calculera l'écart entre le poids
prédit et le poids réellement utilisé.

**Analyse de sensibilité — à faire avant l'entretien.** Faire varier consommation,
contexture et marge sur leurs plages plausibles, et mesurer de combien le poids final
bouge. Ça dit quelles réponses de Justine méritent du temps et lesquelles sont du bruit,
donc dans quel ordre poser les questions. Aucune dépendance, une heure de travail.

Les plages sont maintenant connues : consommation **1 à 2 kg/m²**, contexture **2 à 8
fils/cm**. Le facteur 2 sur la consommation écrase probablement tout le reste — l'analyse
sert alors surtout à le confirmer et à chiffrer de combien. La seule façon de resserrer
est celle du métier : peser un essai tissé de 10 × 10 cm.

## 3. Le test papier

Une heure avec Justine, et le point de contrôle qui tranche. Aucune automatisation ne le
remplace : il faut une imprimante, du scotch et un métier.

Imprimer **deux bandes consécutives**, les assembler, les poser sur le métier dans le
sens d'emploi — à l'envers, contre la chaîne. Puis quatre questions, rien de plus :

1. Tu peux tisser à partir de ce tracé, oui ou non ?
2. Qu'est-ce que tu dois retoucher, et combien de temps ça te prend ?
3. La bande suivante se raccorde-t-elle au cordeau ?
4. Le pas (20 ou 40 cm) est-il le bon pour ce modèle ?

Noter les réponses telles quelles, y compris ce qui gêne sans être bloquant.

Et une question à poser en plus, **sur ce modèle-ci et pas en général** : combien de
temps te prendrait le calque fait main ? L'ordre de grandeur publié va de quelques heures
à plusieurs jours selon la taille et la densité de dégradés — trop large pour servir de
seuil au § 4. C'est la durée sur le modèle du test qui compte.

## 4. Verdict

Le livrable de l'étape 3 n'est pas une démo : c'est un tableau de chiffres et un PDF à
scotcher.

| Critère | Mesure | Si ça ne passe pas |
| --- | --- | --- |
| Tracé tissable | Réponse de Justine, oui / non | Revoir l'extraction de contours avant tout développement |
| Sens du calque | Utilisable tel quel contre la chaîne, oui / non | Corriger le miroir avant tout le reste — c'est un bug, pas un réglage |
| Retouche raisonnable | Temps de retouche < temps du calque fait main *sur ce modèle* (§ 3) | Renforcer F1 (outils de retouche) ou baisser l'ambition du détail auto |
| Raccord des bandes | Écart au cordeau entre deux bandes consécutives | Recouvrement et repères latéraux à revoir, ou réduire le pas |
| Chiffrage | Écart au poids réel des 3 ouvrages | Corriger la table de consommation avec Justine |

Si les cinq passent, le MVP tient et on enchaîne sur l'étape 4 : choix de la stack (le
prototype dira si le traitement tient sur le téléphone ou demande un serveur), puis F1
dans l'app avec le design déjà fait.

Deux chantiers à mener en parallèle, pas à la place : l'entretien d'une heure avec
Justine, réordonné par l'analyse de sensibilité, et un test des maquettes auprès de 4 à 5
étudiants — le canvas est déjà cliquable, trois écrans réagissent.
