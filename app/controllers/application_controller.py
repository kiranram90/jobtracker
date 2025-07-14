from flask import Blueprint, request, jsonify
from app.repositories.job_application_repository import JobApplicationRepository
from app.dto.job_application_dto import JobApplicationDTO
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for



application_bp = Blueprint('application_bp', __name__,)


@application_bp.route('/applications-page', methods=['GET'])
@login_required
def applications_page():
    apps = JobApplicationRepository.get_all()
    return render_template('applications.html', applications=apps)


# This controller handles job application related routes
@application_bp.route('/applcations', methods=['GET'])
@login_required
def get_applications():
    apps = JobApplicationRepository.get_all()
    return jsonify([JobApplicationDTO.from_orm(apps).dict() for app in apps]), 200


@application_bp.route('/applications/new_app', methods=['GET'])
@login_required
def new_application_form():
    return render_template('new_application_form.html')

@application_bp.route('/applications', methods=['POST'])
@login_required
def create_application():
    data = request.form.to_dict()
    data['user_id'] = current_user.id
    if not data or not data.keys():
        return jsonify({"error": "No input data provided"}), 400
    app = JobApplicationRepository.create(data)
    return redirect(url_for('application_bp.applications_page'))

@application_bp.route('/applications/<int:app_id>', methods=['PUT'])
@login_required
def update_application(app_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    app = JobApplicationRepository.get_by_id(app_id)
    if not app:
        return jsonify({"error": "Application not found"}), 404
    JobApplicationRepository.update(app, request.json)
    return jsonify({"message": "Updated"}), 200
    
@application_bp.route('/applications/<int:app_id>', methods=['DELETE'])
@login_required
def delete_application(app_id):
    app = JobApplicationRepository.get_by_id(app_id)
    if not app:
        return jsonify({"error": "Application not found"}), 404
    JobApplicationRepository.delete(app)
    return jsonify({"message": "Application deleted successfully"}), 200