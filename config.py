from sqlmodel import SQLModel, Session, create_engine
import dotenv, os
from database import Database

dotenv.load_dotenv(override=True)

engine = create_engine(os.getenv("DATABASE_URL"))

KEY = os.getenv("SECRET_KEY")


# Dependências
def create_database():
    SQLModel.metadata.create_all(engine)

def get_database():
    db = Database(Session(engine))
    try:
        yield db
    finally:
        db.close()