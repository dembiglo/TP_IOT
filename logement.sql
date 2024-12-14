-- =============================
-- QUESTION 2 : Suppression des tables
-- =============================

-- Supprimer la table Mesure si elle existe
DROP TABLE IF EXISTS Mesure;

-- Supprimer la table Capteur_Actionneur si elle existe
DROP TABLE IF EXISTS Capteur_Actionneur;

-- Supprimer la table Type_Capteur si elle existe
DROP TABLE IF EXISTS Type_Capteur;

-- Supprimer la table Facture si elle existe
DROP TABLE IF EXISTS Facture;

-- Supprimer la table Pièce si elle existe
DROP TABLE IF EXISTS Piece;

-- Supprimer la table Logement si elle existe
DROP TABLE IF EXISTS Logement;

-- =============================
-- QUESTION 3 : Création des tables
-- =============================

-- Table Logement : contient les informations de chaque logement
CREATE TABLE Logement (
    id_logement INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique du logement
    adresse TEXT NOT NULL, -- Adresse obligatoire du logement
    num_telephone TEXT NOT NULL, -- Numéro de téléphone obligatoire
    adresse_IP TEXT NOT NULL, -- Adresse IP obligatoire
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL -- Date d'insertion automatique
);

-- Table Pièce : représente les pièces d'un logement
CREATE TABLE Piece (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique de la pièce
    nom TEXT NOT NULL, -- Nom obligatoire de la pièce (ex., Salon, Chambre)
    coordonnees_3D TEXT NOT NULL, -- Coordonnées obligatoires dans une matrice 3D
    id_logement INTEGER NOT NULL, -- Référence obligatoire au logement
    FOREIGN KEY (id_logement) REFERENCES Logement(id_logement) -- Relation avec Logement
);

-- Table Type_Capteur : liste les types de capteurs/actionneurs
CREATE TABLE Type_Capteur (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique du type
    nom_type TEXT NOT NULL, -- Nom obligatoire du type de capteur/actionneur (ex., Température)
    unite_mesure TEXT NOT NULL, -- Unité de mesure obligatoire associée au type
    plage_precision TEXT NOT NULL -- Plage de précision facultative (ex., 0.1°C) )
    
);

-- Table Capteur_Actionneur : représente les capteurs et actionneurs dans les pièces
CREATE TABLE Capteur_Actionneur (
    id_capteur INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique du capteur/actionneur
    id_type INTEGER NOT NULL, -- Référence obligatoire au type de capteur/actionneur
    reference_commerciale TEXT NOT NULL, -- Référence commerciale obligatoire du capteur/actionneur
    id_piece INTEGER NOT NULL, -- Référence obligatoire à la pièce où se trouve le capteur/actionneur
    port_communication TEXT NOT NULL, -- Port obligatoire utilisé pour communiquer avec le serveur
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Date d'insertion automatique obligatoire
    FOREIGN KEY (id_type) REFERENCES Type_Capteur(id_type), -- Relation avec Type_Capteur
    FOREIGN KEY (id_piece) REFERENCES Piece(id_piece) -- Relation avec Pièce
);

-- Table Mesure : contient les mesures collectées par les capteurs/actionneurs
CREATE TABLE Mesure (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique de la mesure
    valeur FLOAT NOT NULL, -- Valeur mesurée obligatoire (ex., 25.5 pour une température)
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Date et heure obligatoires de la mesure
    id_capteur INTEGER NOT NULL, -- Référence obligatoire au capteur/actionneur ayant enregistré la mesure
    FOREIGN KEY (id_capteur) REFERENCES Capteur_Actionneur(id_capteur) -- Relation avec Capteur_Actionneur
);

-- Table Facture : représente les factures associées à un logement
CREATE TABLE Facture (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique de la facture
    type_facture TEXT NOT NULL, -- Type obligatoire de la facture (ex., Eau, Électricité, Déchets)
    date_facture TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Date obligatoire de la facture
    montant FLOAT NOT NULL, -- Montant obligatoire de la facture
    valeur_consommee FLOAT NOT NULL, -- Valeur consommée facultative (ex., kWh, m3)
    id_logement INTEGER NOT NULL, -- Référence obligatoire au logement correspondant
    FOREIGN KEY (id_logement) REFERENCES Logement(id_logement) -- Relation avec Logement
);

-- =============================
-- QUESTION 4 : Insertion d'un logement avec 4 pièces
-- =============================

-- Insérer un logement
INSERT INTO Logement (adresse, num_telephone, adresse_IP)
VALUES ('123 Rue des Lilas', '0601020304', '192.168.1.1');

-- Insérer 4 pièces pour ce logement
INSERT INTO Piece (nom, coordonnees_3D, id_logement)
VALUES ('Salon', '0,0,0', 1);

INSERT INTO Piece (nom, coordonnees_3D, id_logement)
VALUES ('Chambre', '0,1,0', 1);

INSERT INTO Piece (nom, coordonnees_3D, id_logement)
VALUES ('Cuisine', '1,0,0', 1);

INSERT INTO Piece (nom, coordonnees_3D, id_logement)
VALUES ('Salle de bain', '1,1,0', 1);

-- =============================
-- QUESTION 5 : Création de 4 types de capteurs/actionneurs
-- =============================

-- Type de capteur : Température
INSERT INTO Type_Capteur (nom_type, unite_mesure, plage_precision)
VALUES ('Température', '°C', '0.1-50.0');

-- Type de capteur : Luminosité
INSERT INTO Type_Capteur (nom_type, unite_mesure, plage_precision)
VALUES ('Luminosité', 'Lux', '0-10000');

-- Type de capteur : Humidité

INSERT INTO Type_Capteur (nom_type, unite_mesure, plage_precision)
VALUES ('Humidité', '%', '0-100');

-- Type de capteur : Consommation électrique
INSERT INTO Type_Capteur (nom_type, unite_mesure, plage_precision)
VALUES ('Consommation électrique', 'kWh', '0-1000');

-- =============================
-- QUESTION 6 : Création de 2 capteurs/actionneurs
-- =============================

-- Capteur de température dans le Salon
INSERT INTO Capteur_Actionneur (id_type, reference_commerciale, id_piece, port_communication)
VALUES (1, 'CapteurTemp123', 1, 'Port1');

-- Capteur d'humidité dans la Salle de bain
INSERT INTO Capteur_Actionneur (id_type, reference_commerciale, id_piece, port_communication)
VALUES (3, 'CapteurHum456', 4, 'Port2');

-- =============================
-- QUESTION 7 : Création de 2 mesures par capteur/actionneur
-- =============================

-- Mesures pour le capteur de température
INSERT INTO Mesure (valeur, id_capteur)
VALUES (22.5, 1); -- Température de 22.5°C

INSERT INTO Mesure (valeur, id_capteur)
VALUES (23.1, 1); -- Température de 23.1°C

-- Mesures pour le capteur d'humidité
INSERT INTO Mesure (valeur, id_capteur)
VALUES (45.0, 2); -- Humidité de 45%

INSERT INTO Mesure (valeur, id_capteur)
VALUES (48.5, 2); -- Humidité de 48.5%

-- =============================
-- QUESTION 8 : Création de 4 factures
-- =============================

-- Factures associées au logement
INSERT INTO Facture (type_facture, montant, valeur_consommee, id_logement)
VALUES ('Électricité', 120.50, 350.0, 1);

INSERT INTO Facture (type_facture, montant, valeur_consommee, id_logement)
VALUES ('Eau',  50.25, 15.0, 1);

INSERT INTO Facture (type_facture,  montant, valeur_consommee, id_logement)
VALUES ('Déchets', 30.00, 200, 1);

INSERT INTO Facture (type_facture, montant, valeur_consommee, id_logement)
VALUES ('Gaz', 75.00, 25.5, 1);
