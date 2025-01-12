from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
from fastapi.params import Body
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import  engine
from .Routers import Posts, Users, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#models.Base.metadata.create_all(bind=engine)






app.include_router(Users.router)
app.include_router(Posts.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}





