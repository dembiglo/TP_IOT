from datetime import datetime
from multiprocessing.resource_tracker import getfd
import random
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timedelta



from requests import Session

# Créer l'application FastAPI
app = FastAPI()

# Monter le dossier static pour les fichiers CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")


# Configurer les templates Jinja2
from fastapi.templating import Jinja2Templates

# Spécifiez le dossier "templates"
templates= Jinja2Templates(directory="templates")

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Monter le dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Monter les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurer les templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # Cette route sert la page d'accueil
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/consommation", response_class=HTMLResponse)
async def read_consommation(request: Request):
    # Cette route sert la page consommation
    return templates.TemplateResponse("consommation.html", {"request": request})

@app.get("/capteurs", response_class=HTMLResponse)
async def get_capteurs_page(request: Request):
    return templates.TemplateResponse("capteurs.html", {"request": request})

@app.get("/configuration", response_class=HTMLResponse)
async def configuration_page(request: Request):
    """
    Route pour afficher la page configuration.
    """
    return templates.TemplateResponse("configuration.html", {"request": request})

@app.get("/economies", response_class=HTMLResponse)
async def read_economies_page(request: Request):
    return templates.TemplateResponse("economies.html", {"request": request})



#Exercice 1 

# Fonction pour se  connecter à la base de données
def connect_db():
    conn = sqlite3.connect('mydb.db')
    conn.row_factory = sqlite3.Row
    return conn

# Modèles pour valider les données
class Mesure(BaseModel):
    valeur: float
    id_capteur: int

class Facture(BaseModel):
    type_facture: str
    montant: float
    valeur_consommee: float
    id_logement: int

class CapteurActionneur(BaseModel):
    id_type: int
    reference_commerciale: str
    id_piece: int
    port_communication: str

# Route POST pour ajouter une mesure
@app.post("/api/Mesure")
def post_Mesure(Mesure: Mesure):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO Mesure (valeur, id_capteur) VALUES (?, ?)",
            (Mesure.valeur, Mesure.id_capteur)
        )
        conn.commit()
        return {"message": "Mesure ajoutée avec succès"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            conn.close()

# Route GET pour récupérer les mesures
@app.get("/api/Mesure")
def get_Mesure():
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM Mesure")
        Mesure = [dict(row) for row in c.fetchall()]
        return Mesure
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            conn.close()



# Route POST pour ajouter une facture
@app.post("/api/Facture")
def post_Facture(Facture: Facture):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO Facture (type_facture, montant, valeur_consommee, id_logement)
            VALUES (?, ?, ?, ?)
            """,
            (Facture.type_facture, Facture.montant, Facture.valeur_consommee, Facture.id_logement)
        )
        conn.commit()
        return {"message": "Facture ajoutée avec succès"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            conn.close()

# Route GET pour récupérer les factures
@app.get("/api/Facture")
def get_Facture():
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM Facture")
        Facture = [dict(row) for row in c.fetchall()]
        return Facture
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            conn.close()



           

#Exercice 2

# Route GET pour afficher un graphique en camembert basé sur les factures
@app.get("/chart", response_class=HTMLResponse)
def get_chart():
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT type_facture, SUM(montant) as total FROM Facture GROUP BY type_facture")
        factures = c.fetchall()

        # Préparer les données pour Google Charts
        data = [["Type", "Montant"]]
        for facture in factures:
            data.append([facture["type_facture"], facture["total"]])

        # Générer le contenu HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['corechart']}});
                google.charts.setOnLoadCallback(drawChart);

                function drawChart() {{
                    var data = google.visualization.arrayToDataTable({data});

                    var options = {{
                        title: 'Répartition des factures',
                        pieHole: 0.4, // Pour ajouter un effet de donut si vous voulez
                        is3D: true    // Pour rendre le graphique en 3D
                    }};

                    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

                    chart.draw(data, options);
                }}
            </script>
        </head>
        <body>
            <h1>Camembert des factures</h1>
            <div id="piechart" style="width: 900px; height: 500px;"></div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()



#Exercice3

# Route pour obtenir les prévisions météo sur 5 jours (1 point par jour)
@app.get("/weather", response_class=HTMLResponse)
def get_weather(city: str = "Paris", country: str = "FR"):
    try:
        # Clé API OpenWeatherMap 
        api_key = "48c11c288de9b8496be785465363b9f2"  
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={api_key}&units=metric&lang=fr"

        # Requête vers l'API OpenWeatherMap
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données météo")

        # Récupération des données JSON
        data = response.json()

        # Regrouper les prévisions (1 par jour)
        forecasts = []
        last_date = ""
        for forecast in data["list"]:
            current_date = forecast["dt_txt"].split(" ")[0]  # Extraire la date (AAAA-MM-JJ)
            if current_date != last_date:  # Prendre uniquement une prévision par jour
                forecasts.append({
                    "date": current_date,
                    "temp": forecast["main"]["temp"],
                    "description": forecast["weather"][0]["description"]
                })
                last_date = current_date  # Mettre à jour la dernière date ajoutée
            if len(forecasts) == 5:  # Arrêter après 5 jours
                break

        # Génération du contenu HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Prévisions météo sur 5 jours</title>
        </head>
        <body>
            <h1>Prévisions météo pour {city}, {country}</h1>
            <ul>
        """
        for forecast in forecasts:
            html_content += f"<li>{forecast['date']}: {forecast['temp']}°C - {forecast['description']}</li>"

        html_content += """
            </ul>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")

 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/Capteurs")
def get_all_capteurs():
    from datetime import datetime, timedelta

    now = datetime.now()
    recent_threshold = now - timedelta(hours=24)  # Seuil : 24 heures

    try:
        conn = connect_db()
        c = conn.cursor()

        # Récupérer tous les capteurs
        c.execute("SELECT * FROM Capteur_Actionneur")
        capteurs = c.fetchall()

        result = []
        for capteur in capteurs:
            capteur_id = capteur[0]  # Index de l'ID du capteur

            # Requête pour les mesures récentes
            c.execute(
                """
                SELECT COUNT(*) FROM Mesure
                WHERE id_capteur = ? AND date_insertion >= ?
                """,
                (capteur_id, recent_threshold)
            )
            recent_measure_count = c.fetchone()[0]

            # Journaux pour débogage
            print(f"Capteur ID: {capteur_id}, Seuil: {recent_threshold}, Mesures récentes: {recent_measure_count}")

            # Déterminer l'état du capteur
            etat = "Actif" if recent_measure_count > 0 else "Inactif"

            # Ajouter le capteur avec son état au résultat
            result.append({
                "id_capteur": capteur[0],
                "id_type": capteur[1],
                "reference_commerciale": capteur[2],
                "id_piece": capteur[3],
                "port_communication": capteur[4],
                "date_insertion": capteur[5],
                "etat": etat
            })

        return result

    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur SQLite : {str(e)}")
    except Exception as e:
        print(f"Erreur générale : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur générale : {str(e)}")
    finally:
        if conn:
            conn.close()




@app.post("/api/Capteurs")
def create_capteur(capteur: CapteurActionneur):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO Capteur_Actionneur (id_type, reference_commerciale, id_piece, port_communication) VALUES (?, ?, ?, ?)",
            (capteur.id_type, capteur.reference_commerciale, capteur.id_piece, capteur.port_communication)
        )
        conn.commit()
        return {"message": "Capteur/Actionneur ajouté avec succès"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.put("/api/Capteurs/{id}")
def update_capteur(id: int, capteur: CapteurActionneur):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute(
            """
            UPDATE Capteur_Actionneur 
            SET id_type = ?, reference_commerciale = ?, id_piece = ?, port_communication = ?
            WHERE id_capteur = ?
            """,
            (capteur.id_type, capteur.reference_commerciale, capteur.id_piece, capteur.port_communication, id)
        )
        conn.commit()
        return {"message": "Capteur/Actionneur mis à jour avec succès"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.delete("/api/Capteurs/{id}")
def delete_capteur(id: int):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("DELETE FROM Capteur_Actionneur WHERE id_capteur = ?", (id,))
        conn.commit()
        return {"message": "Capteur/Actionneur supprimé avec succès"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            conn.close()

from sqlalchemy.orm import Session
from fastapi import Depends

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import get_db


@app.get("/api/Economies", response_model=list[dict])
def get_economies(db: Session = Depends(get_db)):
    """
    Calcule les économies réalisées en comparant les montants des factures
    actuelles avec les factures passées.
    """

    # Sélection des factures actuelles (derniers 30 jours)
    factures_actuelles = db.execute(text("""
        SELECT type_facture, SUM(montant) AS montant_actuel
        FROM Facture
        WHERE date_facture >= DATE('now', '-1 month') -- Factures actuelles (1 mois)
        GROUP BY type_facture
    """)).fetchall()

    # Sélection des factures passées (avant 30 jours)
    factures_passees = db.execute(text("""
        SELECT type_facture, SUM(montant) AS montant_passe
        FROM Facture
        WHERE date_facture < DATE('now', '-1 month') -- Factures passées
        GROUP BY type_facture
    """)).fetchall()

    # Conversion des résultats en dictionnaires pour faciliter le traitement
    factures_actuelles_dict = {row['type_facture']: row['montant_actuel'] for row in factures_actuelles}
    factures_passees_dict = {row['type_facture']: row['montant_passe'] for row in factures_passees}

    # Calcul des économies
    economies = []
    for type_facture in set(factures_actuelles_dict.keys()).union(factures_passees_dict.keys()):
        montant_actuel = factures_actuelles_dict.get(type_facture, 0)
        montant_passe = factures_passees_dict.get(type_facture, 0)
        economie = montant_passe - montant_actuel

        economies.append({
            "type_facture": type_facture,
            "montant_actuel": montant_actuel,
            "montant_passe": montant_passe,
            "economie": economie
        })

    return economies





# Point d'entrée pour lancer le serveur
if __name__ == "_main_":
    import uvicorn
    uvicorn.run("exercice1:app", host="127.0.0.1", port=8000, reload=True)
