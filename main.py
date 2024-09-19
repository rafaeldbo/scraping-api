from fastapi import FastAPI, HTTPException, Header, status
import jwt

from database import Database, Usuario, Noticia
from scraper import scraping_g1

db = Database('usuarios', Usuario)
key = 'cloudj'
app = FastAPI()

@app.post('/registrar', status_code=status.HTTP_201_CREATED)
def registrar(usuario: Usuario) -> dict[str, str]:

    if not db.within('email', usuario.email):
        usuario.senha = jwt.encode({'email': usuario.email}, usuario.senha+key)
        db.add(usuario)
        return {'jwt': usuario.senha}
    
    raise HTTPException(409, 'user already exists')

@app.post('/login')
def login(usuario: Usuario) -> dict[str, str]:
    db_usuario = db.get_by('email', usuario.email)

    if db_usuario is None:
        raise HTTPException(401, 'email not recognized')
    
    try:
        if usuario.email != jwt.decode(db_usuario.senha, usuario.senha+key, 'HS256')['email']:
            raise HTTPException(401, 'incorrect password, something is wrong')
    except:
        raise HTTPException(401, 'incorrect password')
    
    return {'jwt': db_usuario.senha}

@app.get('/consultar')
def consultar(Authorization:str|None=Header(default=None)) -> list[Noticia]:
    if Authorization is None or 'Bearer ' not in Authorization:
        raise HTTPException(403, 'authorization not provided')
    
    if not db.within('senha', Authorization.split(' ')[1]):
        raise HTTPException(403, 'incorrect token')
    
    return scraping_g1()