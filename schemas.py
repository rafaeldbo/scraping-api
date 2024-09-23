from pydantic import BaseModel

class Token(BaseModel):
    jwt: str

class Usuario(BaseModel):
    nome:  str | None = None
    email: str
    senha: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str
    
class Noticia(BaseModel):
    titulo: str
    link: str
    tema: str
    tempo_publicacao: str