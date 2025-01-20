from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostRet(**post)
    posts_map = map(validate, res.json())
    #print(posts_map)
    #posts_list = list(posts_map)    
    #print(res.json())
    assert len(res.json())==len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res= client.get("/posts/")
    assert res.status_code ==401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res= client.get("/posts/{test_posts[0].id}")
    assert res.status_code ==401

def test_user_get_posts_does_not_exist(authorized_client, test_posts):
    res= authorized_client.get(f"/posts/9999999999")
    assert res.status_code ==404

def test_get_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostVote(**res.json())
    print(post)
    assert post.Post.id == test_posts[0].id

@pytest.mark.parametrize("title, content, published", [
                          ("awesome title", "awesome new content", True),
                          ("awesome pizza", "i love pizza", True),
                          ("awesome scyscrapper", "awesome new skyscraper", False)])
def test_create_post(authorized_client,test_user,title, content, published):
    res = authorized_client.post("/posts/createposts",json={"Title":title,
                                    "Content":content,"published":published})
    #print("this point", **res)
    created_post = schemas.Posts(**res.json())   
    assert res.status_code == 201
    assert created_post.Title == title
    assert created_post.Content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client,test_user):
    res = authorized_client.post("/posts/createposts",json={"Title":'title',
                                    "Content":'content'})
    #print("this point", **res)
    created_post = schemas.Posts(**res.json())   
    assert res.status_code == 201
    assert created_post.Title == 'title'
    assert created_post.Content == 'content'
    assert created_post.published == True
    

def test_unauthorized_user_create_posts(client, test_user, test_posts):
    res= client.post("/posts/createposts",json={"Title":'title',
                                    "Content":'content'})
    assert res.status_code ==401


def test_unauthorized_user_delete_Posts(client, test_user, test_posts):
    res = client.delete("/posts/delete/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/delete/800000")
    assert res.status_code ==404

def test_delete_other_user_post(authorized_client,test_user, test_posts):
    res = authorized_client.delete(f"/posts/delete/{test_posts[3].id}")

    assert res.status_code == 403

def test_update_post(authorized_client,test_user, test_posts):
    data = {
        "Title":"4rd title",
        "Content":"4rd content",
        "owner_id": test_user['id']
    }
    res = authorized_client.put(f"/posts/update/{test_posts[0].id}",json=data)
    updated_post = schemas.CreatePost(**res.json())
    print("update post", updated_post)
    assert res.status_code == 200
    assert updated_post.Title == data['Title']
    assert updated_post.Content == data['Content']

def test_update_Other_user_post(authorized_client,test_user, test_posts):    
    data={
        "Tile": "Updated title",
        "Content": "Content Updated",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 405

def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/update/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client,test_user, test_posts):
    data={
        "Tile": "Updated title",
        "Content": "Content Updated",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/update/80000", json=data)

    assert res.status_code ==404
