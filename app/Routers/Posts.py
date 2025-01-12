from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  engine, get_db
from .. import models, schemas, utils, oauth
from typing import Optional, List
from sqlalchemy import func
#from sqlalchemy.orm import asdict


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#@router.get("/", response_model=List[schemas.PostRet])
@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db:Session =Depends(get_db), get_current_user :int = Depends(oauth.get_current_user), limit:int=10, skip:int=0, Search:Optional[str]=""):
#    cursor.execute("""select * from \"Posts\"""")
#    posts = cursor.fetchall()
    '''
    posts = db.query(models.Post).filter(models.Post.Title.contains(Search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote,
                        models.Vote.post_id==models.Post.id, isouter =True).group_by(models.Post.id)
    '''
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote,
                        models.Vote.post_id==models.Post.id, isouter =True).group_by(
                            models.Post.id).filter(models.Post.Title.
                                                   contains(Search)).limit(limit).offset(skip).all()
    
    
    return  posts



@router.get("/{id}", response_model=schemas.PostVote)
def get_posts_ind(id:int, db:Session =Depends(get_db),get_current_user :int = Depends(oauth.get_current_user) ):
    # cursor.execute("""select * from \"Posts\" where \"Posts\".id =%s""",(str(id)))
    # post = cursor.fetchone()
    # print(post)
    # #post = get_post(id)
    #post_query = db.query(models.Post).filter(models.Post.id==id)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote,
                        models.Vote.post_id==models.Post.id, isouter =True).group_by(
                            models.Post.id).filter(models.Post.id==id).first()
   
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return response
    
    
    return  posts


@router.post("/createposts",status_code=status.HTTP_201_CREATED, response_model=schemas.PostRet)
def create_post(post:schemas.CreatePost,db:Session =Depends(get_db), get_current_user :int = Depends(oauth.get_current_user)):
    # post = post.dict()
    # print(post)
    # while True:
    #     try:
    #         cursor.execute("""Insert into \"Posts\" (\"Title\", \"Content\") values (%s,%s) Returning *""", (post['title'],post['content']))
    #         conn.commit()
    #         break
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,detail=f"post with {id} not found")
    #         time.sleep(2)
    #print(get_current_user)
    #post = post.dict()
    new_post= models.Post(owner_id = get_current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session =Depends(get_db),get_current_user :int = Depends(oauth.get_current_user)):
    # while True:
    #     try:
    #         cursor.execute("""Delete from \"Posts\" where \"Posts\".id=%s """,(str(id),))
    #         conn.commit()
    #         break
    #     except Exception as error:
    #         raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"Not able to delete {error}")
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post is None:
     raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"Not able to delete ")
    
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"Not Authorized")
     

    post_query.delete(synchronize_session=False)
    db.commit()
    return  {"message": "The posts has been deleted"}


@router.put("/update/{id}", response_model=schemas.PostRet)
def update_post(id:int, post:schemas.Post , db:Session =Depends(get_db),get_current_user :int = Depends(oauth.get_current_user)):
    # print(post)
    # while True:
    #     try:
    #         cursor.execute("""update \"Posts\" set \"Title\" =%s, \"Content\"=%s, \"Published\"=%s where \"Posts\".id = %s
    #             Returning *""",  (post.title,post.content,post.published,str(id)))
    #         post = cursor.fetchone()
    #         conn.commit()
    #         break
    #     except Exception as error:
    #         raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"Not able to delete {error}")
    post_query = db.query(models.Post).filter(models.Post.id==id)
    old_post = post_query.first()
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, 
                            detail=f"Not able to delete ")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
    