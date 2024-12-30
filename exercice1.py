from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests
from pydantic import BaseModel
import sqlite3
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenue dans l'API"}

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


# Point d'entrée pour lancer le serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("exercice1:app", host="127.0.0.1", port=8000, reload=True)
