import requests

# URL de l'API pour ajouter des factures
url = "http://127.0.0.1:8000/api/Facture"

# En-têtes pour la requête HTTP
headers = {"Content-Type": "application/json"}

# Liste des factures à ajouter avec des dates spécifiques
factures = [
    {"type_facture": "Electricité", "montant": 400.50,"valeur_consommee":300.50, "id_logement": 1, "date_facture": "2024-11-10"},
    {"type_facture": "Eau", "montant": 150.00, "valeur_consommee":159.50,"id_logement": 1, "date_facture": "2024-11-10"},
    {"type_facture": "Internet", "montant":130.00, "valeur_consommee":250.00,"id_logement": 1, "date_facture": "2024-11-10"},
    {"type_facture": "Loyer", "montant": 500.00, "valeur_consommee":150.50,"id_logement": 1, "date_facture": "2024-11-10"},
    {"type_facture": "Gaz", "montant": 200.00,"valeur_consommee":350.00, "id_logement": 1, "date_facture": "2024-11-10"},
    {"type_facture": "Assurance", "montant":250.50,"valeur_consommee":200.00, "id_logement": 1, "date_facture": "2024-11-10"},
    {"type_facture": "Déchets", "montant":150.00,"valeur_consommee":254.00, "id_logement": 1, "date_facture": "2024-11-10"},
]

# Boucle pour envoyer les factures une par une
for facture in factures:
    response = requests.post(url, json=facture, headers=headers)
    if response.status_code == 200:
        print(f"Facture ajoutée avec succès : {facture}")
    else:
        print(f"Erreur lors de l'ajout : {facture}")
        print(response.json())
