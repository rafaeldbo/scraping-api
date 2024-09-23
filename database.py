from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import models, schemas

engine = create_engine('postgresql+psycopg2://cloud:1234@localhost:5432/cloud')
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)


class Database():
    session: Session
    table: object

    def __init__(self, session: Session) -> None:
        self.session = session

    def close(self) -> None:
        self.session.close()

    def get(self, table:object, id: int):
        return self.session.query(table).filter(table.id == id).first()

    def get_all(self, offset:int=0, limit:int=100):
        return self.session.query(self.table).offset(offset).limit(limit).all()    

    def create(self, new_object:schemas.BaseModel):
        db_object = self.table(**new_object.model_dump())
        self.session.add(db_object)
        self.session.commit()
        self.session.refresh(db_object)
        return db_object


class UsuarioTable(Database):
    table = models.Usuario

    def get_by_email(self, email:str):
        return self.session.query(models.Usuario).filter(models.Usuario.email == email).first()
    
    def get_by_senha(self, senha:str):
        return self.session.query(models.Usuario).filter(models.Usuario.senha == senha).first()

