from app.models.job_application import JobApplication
from app import db


class JobApplicationRepository():
    @staticmethod
    def get_all():
        return JobApplication.query.all()

    @staticmethod
    def get_by_id(app_id):
        return JobApplication.query.get(app_id)
    
    @staticmethod
    def create(application_data):
        
        new_application = JobApplication(
            user_id=application_data['user_id'],
            job_title=application_data['job_title'],
            company_name=application_data['company_name'],
            posting=application_data['posting'],
            status=application_data.get('status', 'applied'),
            notes=application_data.get('notes', ''),
        )
        db.session.add(new_application)
        db.session.commit()
        return new_application
    
    @staticmethod
    def update(app, data):
        for key, value in data.items():
            setattr(app, key, value)
        db.session.commit()

    @staticmethod
    def delete(app):
        db.session.delete(app)
        db.session.commit()
        
        

    