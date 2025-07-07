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

def test_get_applications(client, app):
    with app.app_context():
        test_and_login(client)


        user = User.query.filter_by(email="test@mail.com").first()
        assert user is not None, "User should be created and logged in"


        client.post("/applications", json={"user_id":  str(user.id),
                                                        "job_title": "Backend Developer",
                                                        "company_name": "OpenAI",
                                                        "posting": "https://openai.com/careers/backend",
                                                        "status": "interview",
                                                        "notes": "Submitted via referral" })
        
        response = client.get("/applications")


    
def test_update_application(client, app):
    with app.app_context():
        test_and_login(client)

        user = User.query.filter_by(email="test@mail.com").first()
        assert user is not None, "User should be created and logged in"

        create_reseponse = client.post("/applications", json={
            "user_id":  str(user.id),
            "job_title": "Backend Developer",
            "company_name": "OpenAI",
            "posting": "https://openai.com/careers/backend",
            "status": "applied",
            "notes": "First version"
        })
        assert create_reseponse.status_code == 201 or create_reseponse.status_code == 200
        
        created_app = JobApplication.query.filter_by(user_id=str(user.id), job_title="Backend Developer").first()
        app_id = created_app.id

        update_response = client.put(f"/applications/{app_id}", json={
            "job_title": "Senior Backend Developer",
            "company_name": "OpenAI",
            "posting": "https://openai.com/careers/backend",
            "status": "interview",
            "notes": "Updated notes"
            })

        assert update_response.status_code == 200
        assert b'Updated' in update_response.data



def test_delete_application(client, app):
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

        created_app = JobApplication.query.filter_by(user_id=str(user.id), job_title="Backend Developer").first()
        app_id = created_app.id

        delete_response = client.delete(f"/applications/{app_id}")

        assert delete_response.status_code == 200
        assert b'Application deleted successfully' in delete_response.data

        









