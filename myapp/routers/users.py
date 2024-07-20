
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body



from typing import List
from .. import models ,schema , utils
from sqlalchemy.orm import Session
from ..database import engine ,SessionLocal, get_db

routers=APIRouter()





@routers.post('/users',status_code=status.HTTP_201_CREATED,response_model=schema.userOut)
async def createUser(user:schema.createUser,db:Session=Depends(get_db)):   
    user.password=utils.hash(user.password)
    newuser=models.User(**user.dict())
    db.add(newuser) 
    db.commit()
    db.refresh(newuser)
    return newuser

@routers.post('/users/{id}',status_code=status.HTTP_201_CREATED,response_model=schema.userOut)
async def updateUser(id:int,user:schema.updateUser,db:Session=Depends(get_db)):
    selectedrow=db.query(models.User).filter(models.User.id==id)
    user.password=utils.hash(user.password)
    print(selectedrow.first())
    if selectedrow.first() is not None:
        selectedrow.update(user.dict(),synchronize_session=False)
        db.commit()
        print('updated rows',selectedrow.first())
        return selectedrow.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no user found with this id{id}')

@routers.get('/users/{id}',response_model=schema.userOut)
async def getUser(id:int,db:Session=Depends(get_db)):
    selectedrow=db.query(models.User).filter(models.User.id==id)
    
    if selectedrow.first() is not None:
        return selectedrow.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'no user found with this id{id}')
