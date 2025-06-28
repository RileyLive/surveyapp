from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
DATABASE_URL = "postgresql://postgres:Stock9100#@localhost/hobbies_database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class HobbyModel(Base):
    __tablename__ = "hobbies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hobby = Column(String)
    inspiration = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic schema
class HobbyEntry(BaseModel):
    name: str
    hobby: str
    inspiration: str

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing, you can later restrict to your Amplify URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/entries")
def get_entries():
    db = SessionLocal()
    entries = db.query(HobbyModel).all()
    db.close()
    return [
        {
            "id": entry.id,
            "name": entry.name,
            "hobby": entry.hobby,
            "inspiration": entry.inspiration
        }
        for entry in entries
    ]

@app.post("/api/entries")
def create_entry(entry: HobbyEntry):
    db = SessionLocal()
    db_entry = HobbyModel(name=entry.name, hobby=entry.hobby, inspiration=entry.inspiration)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    db.close()
    return {"message": "Entry created successfully"}
