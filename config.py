from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

import dotenv, os

dotenv.load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
Base = declarative_base()
Base.metadata.create_all(bind=engine)

KEY = os.getenv("SECRET_KEY")