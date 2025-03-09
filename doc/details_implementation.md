
## Fonctionnement de la base de donnée 

**Echanges effectués quand `send_query()` est appelé sur le client**
```
Client                          Serveur de Base de Données
  |                                           |
  | ------ Connecte via socket -------------> |
  |                                           |
  | --- Envoie longueur des données --------> |
  |                                           |
  | - Envoie données sérialisées par paquet ->|
  |                                           |
  | <------- Envoie statut d'erreur --------- |
  |                                           |
  | <----- Envoie longueur de la réponse ---- |
  |                                           |
  | <--- Envoie réponse par paquet ------     |
  |                                           |
  | -- Le client désérialise les données ---- |
  |                                           |
```

## Fonctionnement de `TimerManager`

La classe `TimerManager` permet de créer et de gérer des minuteries qui exécutent des fonctions après un certain délai. Voici les principales méthodes de cette classe :
minuteries.

- **`create_timer`** : Crée une nouvelle minuterie avec une durée spécifiée, une fonction à exécuter, et des arguments optionnels. La minuterie peut être répétée si nécessaire.
- **`update`** : Met à jour les minuteries en vérifiant si leur durée est écoulée. Si c'est le cas, la fonction associée est exécutée et la minuterie est soit supprimée, soit réinitialisée si elle est répétée.

### Exemple typique d'usage

Supposons que nous voulons créer une minuterie qui affiche un message après 2 secondes. Voici comment nous pourrions utiliser `TimerManager` :

```python
from utils.timermanager import TimerManager

# Initialisation du gestionnaire de minuteries
timer_manager = TimerManager()

# Fonction à exécuter après 2 secondes
def afficher_message():
    print("2 secondes se sont écoulées!")

# Création de la minuterie
timer_manager.create_timer(2.0, afficher_message)

# Boucle principale du programme
while True:
    # Mise à jour du timer
    timer_manager.update()
```

### Cheminement pour l'implémentation

1. **Définition des besoins** : Nous avons identifié le besoin de gérer des minuteries pour exécuter des fonctions après un certain délai, sans utiliser `sleep`, puisque nous devons continuer à executer la boucle principale.
2. **Conception de la classe `TimerManager`** : Nous avons approché le probleme d'une maniere à rendre le minuteur le plus facile d'utilisation possible:
- En s'aidant de la programmation objet, il est facile de mettre en parametre une methode de l'instance d'une classe, une methode conçue pour ne pas prendre de parametre et puiser dans les attributs de la classe pour son fonctionnement.  
Cela permet d'avoir toujours des paramètres "à jour", puisque rentrer les parametre à l'initialisation d'un minuteur ne nous guarantis pas que à l'execution de la fonction une minute plus tard, que les parametre rentrés (comme la position, couleur ...) sont toujours d'actualité.

- L'avantage de `create_timer()`, c'est que l'utilisateur n'a rien besoin de faire de plus, mais à l'inconvenient de devoir etre appelé sur une seule instance la classe `TimerManager`, qui doit donc etre passé en parametre de la fonction qui doit créer un minuteur.  
3. **Test et validation** : Nous avons testé la classe avec différents scénarios pour nous assurer qu'elle fonctionne correctement, nous avons par exemple trouvé un bug qui ne supprimait pas correctement les minuteurs écoulés quand la durée était très courte.