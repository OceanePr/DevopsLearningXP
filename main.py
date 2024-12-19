from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Item
from config import DATABASE_CONFIG

# Configurer la connexion à la base de données PostgreSQL
DATABASE_URL = f"postgresql://{DATABASE_CONFIG['DB_USER']}:{DATABASE_CONFIG['DB_PASSWORD']}@{DATABASE_CONFIG['DB_HOST']}:{DATABASE_CONFIG['DB_PORT']}/{DATABASE_CONFIG['DB_NAME']}"
engine = create_engine(DATABASE_URL)

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Créer une application FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    """Endpoint racine pour tester le serveur."""
    return {"message": "Bienvenue sur FastAPI avec PostgreSQL !"}

@app.post("/items/")
def create_item(name: str, description: str, db: Session = Depends(get_db)):
    """Créer un nouvel élément dans la base de données."""
    item = Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    """Lire tous les éléments de la base de données."""
    return db.query(Item).all()


