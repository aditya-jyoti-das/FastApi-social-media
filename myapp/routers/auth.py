from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from typing import List
from .. import models ,schema , utils
from sqlalchemy.orm import Session
from ..database import engine ,SessionLocal, get_db
from .. import oauth2

routers=APIRouter()


@routers.post('/login',response_model=schema.Token)
async def login(user_creadential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):

    user=db.query(models.User).filter(models.User.email==user_creadential.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    
    if not utils.verify_password(user_creadential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    
    access_token=oauth2.create_access_token(data={'user_id':user.id})

    return {"access_token":access_token,"token_type":"bearer"}

