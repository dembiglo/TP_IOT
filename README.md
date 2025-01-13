# Projet IoT - Documentation

## Contenu de l'archive

L'archive contient les éléments suivants :

1. **Fichiers HTML** :
   - `index.html` : Page d'accueil.
   - `consommation.html` : Affichage des graphiques de consommation.
   - `capteurs.html` : Gestion des capteurs/actionneurs.
   - `economies.html` : Visualisation des économies réalisées.
   - `configuration.html` : Configuration des capteurs/actionneurs.

2. **Scripts JavaScript** :
   - `scripts.js` : Gère les interactions de la page consommation.
   - `capteurs.js` : Gère la page des capteurs/actionneurs.
   - `economies.js` : Gère la page des économies.
   - `configuration.js` : Gère la page de configuration.

3. **Code serveur** :
   - `exercice1.py` : Serveur RESTful développé avec FastAPI.

4. **Base de données** :
   - `mydb.db` : Base de données SQLite contenant les informations nécessaires pour les capteurs, factures, mesures, etc.

5. **README.md** : Ce fichier de documentation.

---

## Configuration du projet

### Prérequis

1. **Python** : Version 3.9 ou supérieure.
2. **Bibliothèques Python** :
   - FastAPI
   - Uvicorn
   - SQLite3
   - Requests
   - Pydantic
   - Jinja2

### Installation des dépendances


### Lancement du serveur

1. Assurez-vous que le fichier `mydb.db` est présent dans le même dossier que `exercice1.py`.
2. Lancez le serveur avec la commande :
   ```bash
   uvicorn exercice1:app --reload
   ```
3. Accédez à l'application via [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Organisation des fichiers par exercices

### Exercice 1 : Gestion des capteurs et mesures
- **Fichier** : `exercice1.py`
- **Routes principales** :
  - POST `/api/Mesure` : Ajoute une nouvelle mesure.
  - GET `/api/Mesure` : Récupère toutes les mesures enregistrées.
  - POST `/api/Facture` : Ajoute une Facture.
  - GET `/api/Facture` : Récupère la liste des factures.

### Exercice 2 : Affichage graphique des factures
- **Fichier** : `exercice1.py`
- **Route principale** :
  - GET `/chart` : Affiche un graphique en camembert des factures par type.
- **Explication** :
  - Les données sont extraites de la table `Facture` dans la base de données SQLite.
  - Le graphique est rendu en HTML avec Google Charts.

### Exercice 3 : Prévisions météo
- **Fichier** : `exercice1.py`
- **Route principale** :
  - GET `/weather?city=Paris&country=FR` : Affiche les prévisions météo pour une ville donnée sur 5 jours.
- **Dépendances** :
  - API OpenWeatherMap (clé API nécessaire).

---

## Fonctionnement des pages web

### 1. Page d'accueil (`index.html`)
- Contient un aperçu du projet et des liens vers les différentes sections.

### 2. Page consommation (`consommation.html`)
- Affiche les données de consommation sous forme de graphique.
- **Problème identifié** : Les données ne sont pas encore triées correctement dans l'ordre chronologique. Cette amélioration reste à finaliser.
- Les données sont gérées avec le script `scripts.js` et récupérées via l'API.

### 3. Page capteurs (`capteurs.html`)
- Permet d'afficher et de surveiller l'état des capteurs.
- Gestion dynamique avec le script `capteurs.js`.

### 4. Page économies (`economies.html`)
- Présente les économies réalisées en comparant les factures actuelles et passées.
- Les calculs sont effectués côté serveur et affichés dynamiquement avec le script `economies.js`.

### 5. Page configuration (`configuration.html`)
- Permet l'ajout, la modification et la suppression de capteurs/actionneurs.
- Gestion des interactions via `configuration.js`.

---

## Sources

1. **Documentation FastAPI** : [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
2. **Google Charts pour les visualisations** : [https://developers.google.com/chart/](https://developers.google.com/chart/)
3. **Bootstrap pour le design** : [https://getbootstrap.com/](https://getbootstrap.com/)
4. **API OpenWeatherMap** : [https://openweathermap.org/api](https://openweathermap.org/api)
5. **SQLite Documentation** : [https://sqlite.org/docs.html](https://sqlite.org/docs.html)
6. **ChatGPT** : Assistance pour la rédaction de code, la documentation et la résolution des problèmes liés au projet.
7. J'ai aussi reçu l'aide de Sekouba et Elsa
---

## Tests et vérifications

1. **Test du serveur** :
   - Accédez à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) pour tester les routes avec l'interface Swagger.
2. **Test des pages web** :
   - Naviguez entre les pages pour vérifier les fonctionnalités dynamiques et graphiques.

---

## Notes supplémentaires

- La clé API pour OpenWeatherMap peut être modifiée directement dans `exercice1.py`.
