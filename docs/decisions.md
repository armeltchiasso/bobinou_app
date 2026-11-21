# Journal des décisions — design

Chaque entrée : ce qui a été arrêté, pourquoi, et ce que ça ferme.
Canvas des maquettes : https://claude.ai/artifact/HquaXAVVUR66cjeBs368AA

## 2026-11-18 · Direction visuelle « Atelier »

Écru, terracotta, indigo de teinture. L'interface reste sourde : seuls le modèle et la
palette de l'ouvrage portent de la couleur saturée, pour ne jamais concurrencer les tons
que l'étudiant doit juger.

Écarté : « outil technique sobre » (neutre, bleu) et « studio contrasté » (sombre).

## 2026-11-18 · Ton friendly

Tutoiement, l'app dit « je », elle encourage sans en faire trop. Boutons en pilule,
rayons plus ronds, pas d'emoji, pas de jargon.

## 2026-11-20 · Logo : une vraie bobine, pas un personnage

La bobine à yeux et sourire est abandonnée. Le logo est une **bobine de laine vue de
trois quarts** : joues en ellipses ouvertes (ratio 0,33, on voit le dessus du disque),
moyeu à rayons, cinq spires bombées, et un brin unique qui passe derrière la bobine à
gauche, traverse la face avant en s'affaissant, puis retombe en volute.

Chemin : V3 (silhouette élancée) → V4 (traitement du fil) → V5 (passage en trois quarts,
d'après une référence fournie) → V6 (six finalistes, E6 retenue) → corrections du brin.

Points de construction qui tiennent le dessin :

- les joues dépassent les spires de 10 unités de chaque côté ;
- chaque spire bombe de 10 vers le bas, même point de vue que les joues ;
- deux passes de fil fines par spire ;
- aucune transparence : cinq valeurs pleines par ton.

Réductions : passes fines jusqu'à 40 px, brin croisé jusqu'à 24 px, silhouette seule à
16 px. Trois dessins pour une seule silhouette.

## 2026-11-20 · Gamme de couleurs du logo (V7)

La laine prend la teinte, **les joues gardent le terracotta** — c'est ce qui fait que les
huit bains restent la même marque. Huit tons : écrue (canonique), indigo, prairie, ocre,
garance, terre, bosquet, ombre. Plus quatre versions une encre.

Règles : l'écrue est la marque par défaut ; l'indigo sert à l'icône sur fond clair et aux
documents imprimés ; les six autres ne s'emploient qu'en vignette de projet, où la bobine
prend le ton dominant de l'ouvrage. Le mot reste encre, jamais dans la couleur de la laine.

## 2026-11-20 · Version indigo posée sur les écrans

Trois tailles selon l'emplacement : 30-32 px sans brin dans les en-têtes, 34 px avec brin
à côté des titres d'étape, 56-76 px avec les passes de fil dans les cartes de bilan.
Sur fond sombre la laine monte d'un cran (`#5A6E94`) ; sur une carte indigo elle passe en
écru.

## 2026-11-20 · Typographie : Young Serif + Space Grotesk

Remplace Fraunces + Inter.

- **Young Serif** pour les titres : serif massif à empattements francs, **une seule
  graisse**. La hiérarchie se fait donc uniquement par la taille — aucun titre en 500 ou
  600, sinon le navigateur fabrique un faux gras qui écrase les empattements.
- **Space Grotesk** pour l'interface et les chiffres. Elle descend de Space Mono, ses
  chasses sont quasi égales : les colonnes de poids et d'écheveaux s'alignent.

Écarté : Raleway (pas de chiffres tabulaires, fûts fins qui grisent sous 13 px),
et les associations « sages » — Spectral, DM Serif, IBM Plex, Instrument Serif, Bitter.
Piste non explorée faute d'hébergement : Redaction, libre, en six grades de dégradation.

## 2026-11-21 · Une version fleurie de la bobine

Un semis de petites fleurs cernées — pétales indigo, cœur terracotta, feuilles vert d'eau
`#BCD9D4` — est posé **sur la laine** et détouré par les joues, de sorte que le motif
tourne avec la bobine. La construction du logo ne change pas : seul le remplissage de la
masse de laine est repris. Trois états : écrue à semis indigo, indigo à semis écru, réserve.

Emploi : écran d'ouverture, première page de la fiche imprimée, étiquette d'écheveau,
communication. Jamais dans un en-tête d'écran de travail, où elle concurrencerait les
couleurs du modèle. Le semis ne descend pas sous **56 px** ; en dessous, la bobine est nue.

La fleurie rejoint la planche V7 (la gamme). La planche d'exploration « V8 — la bobine et
les fleurs » a été supprimée du canvas.

Écarté : la grande fleur unique en face avant, les spires en guirlandes de pétales, le ruban
fleuri, et les cinq greffes qui posaient les fleurs *autour* de la bobine (moyeu en étamines,
brin fleuri, joues en corolle, spires en pétales, bobine dans la fleur). Également écarté :
importer le rose `#EE8FC0` et l'orange `#F4792B` de la référence — la direction Atelier reste
sourde, on n'emprunte que les formes et le vert d'eau.

## En suspens

- **Le fil de progression** (V8 / série V3) : la barre devient un fil qui dessine le
  contour du modèle. Maquetté sur six écrans, **pas encore tranché**. Faiblesse connue :
  à l'étape 1 le fil est presque vide là où une barre à 17 % est plus franche. Correction
  proposée si on le garde : démarrer avec le premier tiers déjà tracé.
- **Le contour dessiné par le fil** : motif constant pour le MVP, silhouette réelle du
  modèle en V2 — quand F1 saura sortir un contour simplifié.
- **Propagation de la typo** : faite sur les séries V2 et V3, la charte v1 et la planche
  de gamme. Restent la charte v2, les deux planches de composants et la série v1.
- Tous les chiffres matière des maquettes restent des placeholders en attente de Justine.
