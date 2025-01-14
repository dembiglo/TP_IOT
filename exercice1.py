from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  # Configurer les templates Jinja2
from fastapi import FastAPI, Request
from fastapi.requests import Request
import requests
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3


# Créer l'application FastAPI
app = FastAPI()

# Monter le dossier static pour les fichiers CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Spécifiez le dossier "templates"
templates= Jinja2Templates(directory="templates")

# Configurer les templates
templates = Jinja2Templates(directory="templates")



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

# Route pour afficher le formulaire
@app.get("/weather", response_class=HTMLResponse)
def get_weather(request: Request, city: str = None, country: str = None):
    forecasts = []  # Par défaut, aucune prévision n'est affichée
    error_message = None

    if city and country:
        try:
            # Clé API OpenWeatherMap
            api_key = "48c11c288de9b8496be785465363b9f2"
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={api_key}&units=metric&lang=fr"

            # Requête vers l'API
            response = requests.get(url)
            if response.status_code != 200:
                error_message = "Erreur : Impossible de récupérer les données météo. Vérifiez la ville et le pays."
            else:
                data = response.json()

                # Filtrer les prévisions (1 par jour sur 5 jours)
                last_date = ""
                for forecast in data["list"]:
                    current_date = forecast["dt_txt"].split(" ")[0]
                    if current_date != last_date:
                        forecasts.append({
                            "date": current_date,
                            "temp": forecast["main"]["temp"],
                            "description": forecast["weather"][0]["description"]
                        })
                        last_date = current_date
                    if len(forecasts) == 5:
                        break
        except Exception as e:
            error_message = f"Erreur : {str(e)}"

    # Retourner la page HTML avec ou sans prévisions
    return templates.TemplateResponse("weather.html", {
        "request": request,
        "city": city,
        "country": country,
        "forecasts": forecasts,
        "error_message": error_message
    })



 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Application Web

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



@app.get("/api/Economies")
def get_economies():
    """
    Calcule les économies réalisées en comparant les montants des factures actuelles avec les montants passés.
    """
    try:
        conn = connect_db()
        c = conn.cursor()

        # Factures actuelles (dernier mois)
        c.execute("""
            SELECT type_facture, SUM(montant) AS montant_actuel
            FROM Facture
            WHERE date_facture >= DATE('now', '-1 month')
            GROUP BY type_facture
        """)
        factures_actuelles = {row[0]: row[1] for row in c.fetchall()}

        # Factures passées (avant le dernier mois)
        c.execute("""
            SELECT type_facture, SUM(montant) AS montant_passe
            FROM Facture
            WHERE date_facture < DATE('now', '-1 month')
            GROUP BY type_facture
        """)
        factures_passees = {row[0]: row[1] for row in c.fetchall()}

        # Calcul des économies
        economies = []
        for type_facture in set(factures_actuelles.keys()).union(factures_passees.keys()):
            montant_actuel = factures_actuelles.get(type_facture, 0)
            montant_passe = factures_passees.get(type_facture, 0)
            economie = montant_passe - montant_actuel

            economies.append({
                "type_facture": type_facture,
                "montant_passe": montant_passe,
                "montant_actuel": montant_actuel,
                "economie": economie
            })

        return economies

    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            conn.close()





# Point d'entrée pour lancer le serveur
if __name__ == "_main_":
    import uvicorn
    uvicorn.run("exercice1:app", host="127.0.0.1", port=8000, reload=True)
