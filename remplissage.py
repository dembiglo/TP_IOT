
import sqlite3
import random

# Initialisation de la base de données et création de la connexion
conn = sqlite3.connect('mydb.db')  # Connexion à la base SQLite
conn.row_factory = sqlite3.Row
c = conn.cursor()  # Permet d'exécuter des requêtes SQL

# Génération des mesures aléatoires
id_capteur = random.randint(1, 2)  # Sélection aléatoire de l'ID du capteur
N = 20  # Nombre d'échantillons à générer

if id_capteur== 1:
    Mesures = [round(random.uniform(20.0, 50.0), 2) for _ in range(N)]
else:
    Mesures = [round(random.uniform(50.0, 100.0), 2) for _ in range(N)]

# Insertion des mesures dans la table "Mesure"
insert_mesures = "INSERT INTO Mesure (valeur, id_capteur) VALUES (?, ?)"
for valeur in Mesures:
    c.execute(insert_mesures, (valeur, id_capteur))

# Validation des modifications pour la table "Mesure"
conn.commit()

# Définition des types de factures possibles
type_facture = [
    "Eau",
    "Electricité",
    "Loyer",
    "Déchets",
    "Internet",
    "Assurance"
]

# Génération et insertion des factures aléatoires
insert_factures = """
INSERT INTO Facture (Type_facture, montant, Valeur_consommee, id_logement) 
VALUES (?, ?, ?, ?)
"""
for _ in range(N):
    c.execute(
        insert_factures,
        (
            random.choice(type_facture),  # Type de facture choisi aléatoirement
            round(random.uniform(20.0, 200.0), 1),  # Montant aléatoire
            round(random.uniform(50.0, 250.0), 1),  # Valeur consommée aléatoire
            random.randint(1, 2)  # ID du logement associé
        )
    )

# Validation des modifications pour la table "Facture" et fermeture de la connexion
conn.commit()
conn.close()
