import pytest
from app.main import app
from sqlalchemy import create_engine
import pytest
from app import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
from app import  database
from app.config import settings
from app.oauth import create_access_token
from app.database import Base
from alembic.config import command




SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind=engine)

TesingSessionLocal  = sessionmaker(autocommit= False, autoflush=False, bind =engine)





@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TesingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[database.get_db] = override_get_db
    #command.upgrade("head")
    yield TestClient(app)
    #command.downgrade("base")

@pytest.fixture
def test_user1(client):
    user_data = {"email":"1234@email.com", "password":"123"}
    res = client.post("/Users/", json=user_data)
    assert res.status_code ==201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email":"123@email.com", "password":"123"}
    res = client.post("/Users/", json=user_data)
    assert res.status_code ==201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id'] })


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user,session, test_user1):
    posts_data = [{"Title":"first title",
                   "Content":"first content",
                   "owner_id": test_user['id']},
                   {"Title":"2nd title",
                   "Content":"2nd content",
                   "owner_id": test_user['id']},
                   {"Title":"3rd title",
                   "Content":"3rd content",
                   "owner_id": test_user['id']},
                   {"Title":"4rd title",
                   "Content":"4rd content",
                   "owner_id": test_user1['id']}  
                   ]
    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                   models.Post(title="3rd title", content="3rd content", owner_id=test_user['id']),
    #                   models.Post(title="2rd title", content="2rd content", owner_id=test_user['id'])])
    
    session.commit()

    posts = session.query(models.Post).all()
    return posts
