from pydantic import BaseModel
from typing import Union
import json, os

class Usuario(BaseModel):
    nome:  Union[str, None] = None
    email: str
    senha: str

    def toJSON(self) -> dict[str, str]:
        return {'nome': self.nome, 'email': self.email, 'senha': self.senha}
    
    def fromJSON(usuario:dict[str, str]) -> BaseModel:
        return Usuario(**usuario)
    
class Noticia(BaseModel):
    titulo: str
    link: str
    tema: str
    tempo_publicacao: str

    def toJSON(self) -> dict[str, str]:
        return {'titulo': self.titulo, 'link': self.link, 'tema': self.tema, 'tempo_publicacao': self.tempo_publicacao}
    
    def fromJSON(noticia:dict[str, str]) -> BaseModel:
        return Noticia(**noticia)
    
class Database():
    def __init__(self, filename: str, object_type: BaseModel) -> None:
        self.file = f'./{filename}.json'
        if not os.path.exists(self.file):
            with open(self.file, 'w') as file:
                file.write('[]')
        self.object = object_type
    
    def load(self) -> dict[str, str]:
        with open(self.file, 'r', encoding='UTF-8') as file:
            return json.loads(file.read())

    def add(self, new_object: any) -> None:
        data = self.load()
        data.append(new_object.toJSON())
        with open(self.file, 'w', encoding='UTF-8') as file:
            file.write(json.dumps(data, indent=4))
    
    def get_by(self, field:str, value:str) -> any:
        return next((self.object.fromJSON(object_data) for object_data in self.load() if object_data[field] == value), None)
    
    def within(self, field:str, value:str) -> bool:
        return next((True for object_data in self.load() if object_data[field] == value), False)



