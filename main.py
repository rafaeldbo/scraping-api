from fastapi import FastAPI, HTTPException, status, Header, Depends

import jwt
from hashlib import sha256

from database import UsuarioTable, SessionLocal
import schemas, scraper
from config import KEY


app = FastAPI()

# Dependency
def get_db():
    db = UsuarioTable(SessionLocal())
    try:
        yield db
    finally:
        db.close()

@app.post('/registrar', status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
def registrar(usuario:schemas.Usuario, db:UsuarioTable=Depends(get_db)) -> dict[str, str]:

    if not db.get_by_email(usuario.email):
        usuario.senha = sha256(usuario.senha.encode()).hexdigest()
        print(usuario.senha)
        db.create(usuario)
        return {'jwt': jwt.encode({'email': usuario.email}, KEY, 'HS256')}
    
    raise HTTPException(409, 'user already exists')

@app.post('/login', response_model=schemas.Token)
def login(usuario:schemas.UsuarioLogin, db:UsuarioTable=Depends(get_db)) -> dict[str, str]:
    db_usuario = db.get_by_email(usuario.email)

    if db_usuario is None:
        raise HTTPException(401, 'email not recognized')
    
    if db_usuario.senha != sha256(usuario.senha.encode()).hexdigest():
        raise HTTPException(401, 'incorrect password')

    return {'jwt': jwt.encode({'email': usuario.email}, KEY, 'HS256')}

@app.get('/consultar', response_model=list[schemas.Noticia])
def consultar(Authorization:str|None=Header(default=None)) -> list[schemas.Noticia]:
    print(Authorization)
    if Authorization is None or 'Bearer ' not in Authorization:
        raise HTTPException(403, 'authorization not provided')
    
    try:
        jwt.decode(Authorization.split(' ')[1], KEY, 'HS256')
    except:
        raise HTTPException(403, 'invalid token')

    scrap = scraper.g1()
    if scrap is None:
        raise HTTPException(408, 'the request exceeded the waiting time')
    return scrap