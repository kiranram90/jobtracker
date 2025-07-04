import json     
from app.models import User, JobApplication
from app import db



def test_and_login(client):
    #register
    client.post("/auth/register", json={
        "email": "test@mail.com",
        "password": "testpassword"
    })
    #login
    client.post("/auth/login", json={
        "email": "test@mail.com",
        "password": "testpassword"
    })


def test_create_application(client, app):
    with app.app_context():
        test_and_login(client)

        user = User.query.filter_by(email="test@mail.com").first()
        assert user is not None, "User should be created and logged in"


        response = client.post("/applications", json={"user_id":  str(user.id),
                                                        "job_title": "Backend Developer",
                                                        "company_name": "OpenAI",
                                                        "posting": "https://openai.com/careers/backend",
                                                        "status": "interview",
                                                        "notes": "Submitted via referral"
                                        })
    assert response.status_code == 201 or response.status_code == 200
    assert b'Application created successfully' in response.data
    










