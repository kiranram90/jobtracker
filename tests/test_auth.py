import json     
from app.models.users import User
from app import db

def test_register(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

    # Confirm user exists
    user = User.query.filter_by(email="test@example.com").first()
    assert user is not None

def test_login(client):

    client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "loginpassword"
    })

    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "loginpassword"
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data



