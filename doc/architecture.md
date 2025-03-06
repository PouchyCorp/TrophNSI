Le projet est divisé en plusieurs modules, chacun s'occupant d'une partie spécifique du jeu. Les principaux modules comprennent :

**Les Modules de Base (Core)** : Responsables de la logique principale du jeu, de la gestion des états et des fonctionnalités de base.

**Les Modules d'Interface Utilisateur (UI)** : Gèrent les éléments de l'interface utilisateur tels que l'inventaire, les boutons et les popups.

**Les Modules d'Objets (Objects)** : Définissent les différents objets qui peuvent être placés dans le jeu et leurs comportements.

**Les Modules Utilitaires (Utils)** : Fournissent des fonctions et des classes utiles pour les coordonnées, les animations et d'autres fonctions d'aide.

Chaque module clé a ses propres responsabilités :

### Les Modules de Base incluent
- **[main.py](/sources/main.py)** (chargement de la configuration et lancement du jeu)
- **[logic.py](/sources/core/logic.py)** (boucle principale du jeu)
- **[room.py](/sources/core/room.py)** (gestion des objets dans la pièce)
- **[spectator.py](/sources/core/spectator.py)** (visualise en lecture seule une sauvegarde)
- **[unlockmanager.py](/sources/core/unlockmanager.py)** (gestion et stockage de la progression du joueur)

### Les Modules d'Interface Utilisateur
- **[inventory.py](/sources/ui/inventory.py)** (gestion de l'inventaire)
- **[button.py](/sources/ui/button.py)** (éléments de bouton)
- **[infopopup.py](/sources/ui/infopopup.py)** (popups d'information)

### Les Modules d'Objets
- **[placeable.py](/sources/objects/placeable.py)** (classe de base des objets placés)
- **[placeablesubclass.py](/sources/objects/placeablesubclass.py)** (sous-classes d'objets avec des comportements spécifiques) 
- **[canva.py](/sources/objects/canva.py)** (gestion du système de peinture)
- **[patterns.py](/sources/objects/patterns.py)** (stockage et )

### Les Modules Utilitaires
- **[coord.py](/sources/utils/coord.py)** (systeme de coordonnées)
- **[anim.py](/sources/utils/anim.py)** (animations)
- **[sound.py](/sources/utils/sound.py)** (effets sonores).

Nous pensons architecture modulaire permet une gestion efficace du jeu, facilitant la maintenance et les extensions.

# Pour plus d'information sur le déroulé du code, regardez timeline.md