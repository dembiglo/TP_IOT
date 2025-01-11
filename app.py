from cProfile import label
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from collections import defaultdict
import sqlite3  # Pour accéder à votre base de données

# Connexion à la base de données SQLite
conn = sqlite3.connect("mydb.db", check_same_thread=False)

app = FastAPI()

# Monter le dossier "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurer les templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




from collections import defaultdict
from datetime import datetime

@app.get("/api/Facture")
def get_factures(time_scale: str = "week"):
    try:
        query = "SELECT date_facture, type_facture, valeur_consommee FROM Facture"
        result = conn.execute(query).fetchall()

        # Groupement des données par période et type de facture
        grouped_data = defaultdict(lambda: defaultdict(float))  # Période -> Type -> Total

        for row in result:
            date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            if time_scale == "day":
                period = date.strftime("%Y-%m-%d")
            elif time_scale == "week":
                period = f"{date.year}-W{date.strftime('%U')}"  # Semaine
            elif time_scale == "month":
                period = date.strftime("%Y-%m")
            
            grouped_data[period][row[1]] += row[2]  # Ajoute la valeur consommée

        # Préparation des données pour le frontend
        response = [
            {
                "periode": period,
                "types": [{"type": type_facture, "valeur": valeur} for type_facture, valeur in types.items()]
            }
            for period, types in grouped_data.items()
        ]

        return response
    except Exception as e:
        print("Erreur lors de la récupération des factures :", e)
        return {"error": "Erreur lors de la récupération des factures."}


@app.get("/grapheConso", response_class=HTMLResponse)
def graphe_conso(request: Request, periode: str = "an", asked: str = "conso"):
    # Code déjà fourni pour préparer les données et afficher la page.
    return templates.TemplateResponse("consommation.html", {
        "request": request,
        "labels": label,
        "consoEau": ["Eau"],
        "consoElectricité": ["Electricité"],
        "consoDéchets": ["Déchets"],
        "consoLoyer": ["Loyer"],
        "consoInternet": ["Internet"],
        "consoAssurance": ["Assurance"]
    })



@app.get("/capteurs", response_class=HTMLResponse)
def capteurs(request: Request):
    try:
        return templates.TemplateResponse("capteurs.html", {"request": request})
    except Exception as e:
        print("Erreur :", e)
        return HTMLResponse(content=f"<h1>Erreur : {e}</h1>", status_code=500)




@app.get("/api/capteurs")
def get_capteurs():
    try:
        query = """
            SELECT 
                ca.id_capteur, tc.nom_type, ca.reference_commerciale, 
                ca.port_communication, ca.date_insertion,
                MAX(m.date_insertion) AS last_measure_date
            FROM Capteur_Actionneur ca
            JOIN Type_Capteur tc ON ca.id_type = tc.id_type
            LEFT JOIN Mesure m ON ca.id_capteur = m.id_capteur
            GROUP BY ca.id_capteur, tc.nom_type, ca.reference_commerciale, 
                     ca.port_communication, ca.date_insertion
        """
        result = conn.execute(query).fetchall()

        capteurs = []
        for row in result:
            # Convertir la dernière date de mesure
            last_measure_date = row[5]
            if last_measure_date:
                last_measure_date = datetime.strptime(last_measure_date, '%Y-%m-%d %H:%M:%S')

            # Déterminer l'état du capteur
            if last_measure_date and (datetime.now() - last_measure_date) < timedelta(days=1):
                etat = "Actif"
            else:
                etat = "Inactif"

            capteurs.append({
                "id_capteur": row[0],
                "nom_type": row[1],
                "reference_commerciale": row[2],
                "port_communication": row[3],
                "date_insertion": row[4],
                "etat": etat
            })

        return capteurs
    except Exception as e:
        print("Erreur lors de la récupération des capteurs :", e)
        return {"error": "Erreur lors de la récupération des capteurs."}



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Point d'entrée pour lancer le serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8001, reload=True)
