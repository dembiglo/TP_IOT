from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Monter le dossier "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurer les templates
templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/consommation", response_class=HTMLResponse)
def consommation(request: Request):
    try:
        return templates.TemplateResponse("consommation.html", {"request": request})
    except Exception as e:
        print("Erreur :", e)  # Affiche l'erreur exacte dans la console
        return HTMLResponse(content=f"<h1>Erreur : {e}</h1>", status_code=500)
    
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