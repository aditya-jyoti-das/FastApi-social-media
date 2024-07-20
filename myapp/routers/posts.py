
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy import func

from typing import List,Optional
from .. import models ,schema , utils
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2

routers=APIRouter()


# @routers.get('/posts',response_model=List[schema.Posts])
@routers.get('/posts',response_model=List[schema.PostOut])
async def getposts(db:Session=Depends(get_db), 
                      get_current_user:int=Depends(oauth2.get_current_user),
                      limit:int=5,
                      skip:int=0,
                      search:Optional[str]=""
                      ):
    # cursor = conn.cursor()
    # query = """
    #         SELECT * FROM Posts;
    #         """
    # cursor.execute(query)
    # myposts=cursor.fetchall()
    # myposts=db.query(models.Posts).filter(models.Posts.title.contains(search) ).offset(skip).limit(limit).all()
    
    result=db.query(models.Posts,func.count(models.Vote.post_id).label('votes')).join(
        models.Vote,models.Posts.id==models.Vote.post_id,isouter=True).group_by(models.Posts.id).filter(
            models.Posts.title.contains(search) ).offset(skip).limit(limit).all()

    return result



@routers.post('/posts',status_code=status.HTTP_201_CREATED,response_model=schema.Posts)
async def createPosts(payload:schema.CreatePost,db:Session=Depends(get_db), 
                      get_current_user:int=Depends(oauth2.get_current_user)):   
    # query="""
    #     insert into Posts(title,content,published,rating) values (%s,%s,%s,%s);
    #     """
    # cursor=conn.cursor()
    # cursor.execute(query,(payload.title,payload.content,payload.published,payload.rating))
    # cursor.execute('select * from Posts where id =(select max(id) from Posts);')
    # userLastPost=cursor.fetchone()
    # conn.commit()
    # newpost=models.Posts(title=payload.title,content=payload.content,published=payload.published)
    
    newpost=models.Posts(owner_id=get_current_user.id,**payload.dict())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)


    return newpost

# @app.get('/posts/latestpost')
# async def getLatestPosts():
#     cursor=conn.cursor()
#     cursor.execute("""select * from Posts where id=(select max(id) from Posts);""")
#     latestpost=cursor.fetchone()
#     conn.commit()
    
#     return {'data':latestpost}



@routers.get('/posts/{id}',response_model=schema.PostOut)
async def getPosts_id(id:int,db:Session=Depends(get_db), 
                      get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor=conn.cursor()
    # cursor.execute(""" select * from Posts where id=%s;""",(id,))
    # posts=cursor.fetchone()

    
    result=db.query(models.Posts,func.count(models.Vote.post_id).label('votes')).join(
        models.Vote,models.Posts.id==models.Vote.post_id,isouter=True).group_by(
            models.Posts.id).filter(models.Posts.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'posts with id {id}, was not found')
    return result




@routers.delete('/posts/{id}')
async def deletePost(id:int,db:Session=Depends(get_db), 
                      get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor=conn.cursor()
    # cursor.execute(""" delete from Posts where id=%s;""",(id,))
    # conn.commit()
    post= db.query(models.Posts).filter(models.Posts.id==id)
    

    # if cursor.rowcount:
    if post.first():
        if post.first().owner_id==get_current_user.id:
            post.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='you are not authorized to perform this operation')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post was not found with id{id}')


@routers.put('/posts/{id}',response_model=schema.Posts)
async def Update_post(id:int,posts:schema.CreatePost,db:Session=Depends(get_db), 
                      get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor=conn.cursor()
    # cursor.execute(""" update Posts set title=%s, content=%s, published=%s, rating=%s where id=%s;""",(posts.title,posts.content,posts.published,posts.rating,id))
    # conn.commit()
    selectedrow=db.query(models.Posts).filter(models.Posts.id==id)

    # if cursor.rowcount:
    if selectedrow.first() is not None:
        if selectedrow.first().owner_id==get_current_user.id:
                
            selectedrow.update(posts.dict(),synchronize_session=False)
            db.commit()
            return selectedrow.first()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are not authorized to perform this operation")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post  was not found with id{id}')

