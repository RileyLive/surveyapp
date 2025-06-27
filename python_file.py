from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
DATABASE_URL = "postgresql://postgres:Stock9100#@localhost/hobbies_database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# SQLAlchemy model
class HobbyModel(Base):
    __tablename__ = "hobbies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hobby = Column(String)
    inspiration = Column(String)

Base.metadata.create_all(bind=engine)

# GraphQL type
@strawberry.type
class HobbyEntry:
    name: str
    hobby: str
    inspiration: str

# GraphQL Query
@strawberry.type
class Query:
    @strawberry.field
    def get_hobbies(self) -> list[HobbyEntry]:
        db = SessionLocal()
        hobbies = db.query(HobbyModel).all()
        db.close()
        return [HobbyEntry(name=h.name, hobby=h.hobby, inspiration=h.inspiration) for h in hobbies]

# GraphQL Mutation
@strawberry.type
class Mutation:
    @strawberry.mutation
    def submit_hobby(self, name: str, hobby: str, inspiration: str) -> HobbyEntry:
        db = SessionLocal()
        entry = HobbyModel(name=name, hobby=hobby, inspiration=inspiration)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        db.close()
        return HobbyEntry(name=entry.name, hobby=entry.hobby, inspiration=entry.inspiration)

# Strawberry schema and app setup
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")
