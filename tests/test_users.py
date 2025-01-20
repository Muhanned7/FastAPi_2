from app import schemas
from fastapi import status
import jwt
from app.config import settings
import pytest


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == "Binding works!!!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/Users", json={"email":"john40@remail.com","password":"123"})
    new_user = schemas.Ret_user(**res.json())
    assert new_user.email == "john40@remail.com"
    assert res.status_code == status.HTTP_201_CREATED

def test_login_user(client, test_user):
    res = client.post("/login", data={"username":test_user['email'],"password":test_user['password']})
    print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key, algorithms={settings.algorithm})
    id:int = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bear token"
    assert res.status_code == 200


def test_failed_user_login(client, test_user):
    res = client.post('/login', data = {'username':test_user['email'],'password': 'wrong password'})
    
    assert res.status_code == 403
    assert res.json().get('detail') == "Invalid credentials"


@pytest.mark.parametrize("email, password, status_code",[
    ('wrongfmail@gmqail.com', '123',403),
    ('123@email.com', '145',403),
    ('worngeamql@email.com ', '1456',403),
    (None, '123', 422),
    ('123@email.com', None,422) 
    ])
def test_incorrect_login(test_user, client,email,password, status_code):
    res = client.post(
        "/login", data={"username":email, "password" : password}
    )
    assert res.status_code == status_code
    
