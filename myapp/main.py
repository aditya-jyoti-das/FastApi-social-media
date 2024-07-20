from fastapi import FastAPI, Depends

from . import models
from .database import engine , get_db
from .routers import posts,users,auth,vote
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()




models.Base.metadata.create_all(bind=engine)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.routers)
app.include_router(users.routers)
app.include_router(auth.routers)
app.include_router(vote.routers)


@app.get('/')
async def root():
    return {'message':"welcome to this api. i hope that you will like this"}  


