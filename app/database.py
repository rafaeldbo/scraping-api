from sqlmodel import SQLModel, Session, select
import models


class Database():
    def __init__(self, session: Session) -> None:
        self.session = session

    def close(self) -> None:
        self.session.close()
        
    def get_all(self, table:SQLModel, offset:int=0, limit:int=100) -> list[SQLModel]:
        return self.session.exec(select(table).offset(offset).limit(limit)).all()
    
    def get(self, table:SQLModel, id: int) -> SQLModel | None:
        return self.session.exec(select(table).where(table.id == id)).first()
    
    def get_where(self, table:SQLModel, conditions:list[bool], first:bool=True) -> list[SQLModel]:
        result = self.session.exec(select(table).where(conditions))
        return result.first() if first else result.all() 

    def create(self, instance:SQLModel) -> None:
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance
    
    def delete(self, table:SQLModel, id:int) -> None:
        instance = self.get(table, id)
        self.session.delete(instance)
        self.session.commit()

    def delete_all(self, table:SQLModel) -> None:
        instances = self.get_all(table)
        for instance in instances:
            self.session.delete(instance)
        self.session.commit()