from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body


from typing import List,Optional
from .. import models ,schema , utils
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from ..database import get_db

routers=APIRouter()


@routers.post('/vote',status_code=status.HTTP_201_CREATED)
async def vote(vote:schema.Vote,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    post=db.query(models.Posts).filter(models.Posts.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" post with the id {vote.post_id} does not exist")



    vote_query=db.query(models.Vote).filter(
        models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id
    )

    found_data=vote_query.first()

    if vote.dir==1:
        if found_data:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'you have already have voted on this post {vote.post_id}')
        else:
            newvote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
            db.add(newvote)
            db.commit()
            return {'message':f'Sucessfully added vote to the post {vote.post_id}'}
        
    else:
        if not found_data:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'you have not voted yet')
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {'message':'sucessfully deleted your vote'}
        

        