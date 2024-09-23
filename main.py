from fastapi import FastAPI, HTTPException, status, Header, Depends

import jwt

from database import UsuarioTable, SessionLocal, engine
import models, schemas, scraper

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
KEY = 'cloudj'

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
        usuario.senha = jwt.encode({'email': usuario.email}, usuario.senha+KEY)
        db.create(usuario)
        return {'jwt': usuario.senha}
    
    raise HTTPException(409, 'user already exists')

@app.post('/login', response_model=schemas.Token)
def login(usuario:schemas.UsuarioLogin, db:UsuarioTable=Depends(get_db)) -> dict[str, str]:
    db_usuario = db.get_by_email(usuario.email)

    if db_usuario is None:
        raise HTTPException(401, 'email not recognized')
    
    try:
        if usuario.email != jwt.decode(db_usuario.senha, usuario.senha+KEY, 'HS256')['email']:
            raise HTTPException(401, 'incorrect password, something is wrong')
    except:
        raise HTTPException(401, 'incorrect password')
    
    return {'jwt': db_usuario.senha}

@app.get('/consultar', response_model=list[schemas.Noticia])
def consultar(Authorization:str|None=Header(default=None), db:UsuarioTable=Depends(get_db)) -> list[schemas.Noticia]:
    if Authorization is None or 'Bearer ' not in Authorization:
        raise HTTPException(403, 'authorization not provided')
    
    if not db.get_by_senha(Authorization.split(' ')[1]):
        raise HTTPException(403, 'incorrect token')
    
    scrap = scraper.g1()
    if scrap is None:
        raise HTTPException(408, 'the request exceeded the waiting time')
    return scrap