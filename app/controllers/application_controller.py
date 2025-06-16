from flask import Blueprint, request, jsonify
from repositories.job_application_repository import JobApplicationRepository
from dto.job_application_dto import JobApplicationDTO

application_bp = Blueprint('application_bp', __name__)



@application_bp.route('/applcations', methods=['GET'])
def get_applications():
    apps = JobApplicationRepository.get_all()
    return jsonify([JobApplicationDTO.from_orm(apps).dict() for app in apps]), 200


@application_bp.route('/application', methods=['POST'])
def create_application():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    app = JobApplicationRepository.create(data)
    return jsonify({"id" : app.id, "message": "Application created successfully"}), 201