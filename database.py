from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Remplacez l'URL ci-dessous par celle de votre base de données
DATABASE_URL = "sqlite:///./mydb.db"  # Exemple pour une base de données SQLite

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance FastAPI pour la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
