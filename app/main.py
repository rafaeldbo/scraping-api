from fastapi import FastAPI, HTTPException, status, Depends, Security
from fastapi.security.api_key import APIKeyHeader

import jwt
from hashlib import sha256
from pydantic import validate_email

from config import KEY, Database, create_database, get_database
from models import User, UserLogin, Token, News
from scraper import g1

app = FastAPI()

@app.on_event('startup')
def on_startup() -> None:
    create_database()


@app.post('/registrar', status_code=status.HTTP_201_CREATED, response_model=Token)
def registrar(usuario: User, db: Database=Depends(get_database)) -> Token:
    
    try:
        validate_email(usuario.email)
    except:
        raise HTTPException(401, 'Invalid email format')

    if not db.get_where(User, User.email == usuario.email):
        usuario.senha = sha256(usuario.senha.encode()).hexdigest()
        db.create(usuario)
        return {'jwt': jwt.encode({'email': usuario.email}, KEY, 'HS256')}
    
    raise HTTPException(409, 'user already exists')

@app.post('/login', response_model=Token)
def login(usuario: UserLogin, db: Database=Depends(get_database)) -> Token:
    
    try:
        validate_email(usuario.email)
    except:
        raise HTTPException(401, 'Invalid email format')
    
    hash_password = sha256(usuario.senha.encode()).hexdigest()
    usuario = db.get_where(User, User.email == usuario.email, first=True)

    if usuario is None:
        raise HTTPException(401, 'email not recognized')
    if usuario.senha != hash_password:
        raise HTTPException(401, 'incorrect password')

    return {'jwt': jwt.encode({'email': usuario.email}, KEY, 'HS256')}

@app.get('/consultar', response_model=list[News])
def consultar(Authorization: str=Security(APIKeyHeader(name="Authorization"))) -> list[News]:
    if Authorization is None or 'Bearer ' not in Authorization:
        raise HTTPException(403, 'authorization not provided')
    try:
        jwt.decode(Authorization.split(' ')[1], KEY, 'HS256')
    except:
        raise HTTPException(403, 'invalid token')

    scrap = g1()
    if scrap is None:
        raise HTTPException(408, 'the request exceeded the waiting time')
    return scrap