from flask import Blueprint, request, jsonify
from app.repositories.job_application_repository import JobApplicationRepository
from app.dto.job_application_dto import JobApplicationDTO
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for
from PyPDF2 import PdfReader


application_bp = Blueprint('application_bp', __name__,)


@application_bp.route('/upload_job_post', methods=['GET', 'POST'])
@login_required
def upload_job_post():
    if request.method == 'POST':
        uploaded_file = request.files('job_post')
        resume_file = request.form('resume_bullets')

        if uploaded_file.endswith('.pdf'):
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = uploaded_file.read().decode('utf-8')


        feedback = get_resume_feedback(job_text=text,resume_bullets = resume_file)

        return render_template('feedback.html', feedback=feedback)

    return render_template('upload_job_post.html') 


def get_resume_feedback(job_text, resume_bullets):
    




def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text
    


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


@application_bp.route('/applications/<int:app_id>')
@login_required
def edit_application_form(app_id):
    app = JobApplicationRepository.get_by_id(app_id)
    return render_template('new_application_form.html', application=app)

@application_bp.route('/applications', methods=['POST', 'GET'])
@login_required
def create_application():
    data = request.form.to_dict()
    data['user_id'] = current_user.id
    if not data or not data.keys():
        return jsonify({"error": "No input data provided"}), 400
    app = JobApplicationRepository.create(data)
    return redirect(url_for('application_bp.applications_page')), 201

@application_bp.route('/applications/<int:app_id>', methods=['POST'])
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
    
@application_bp.route('/applications/<int:app_id>', methods=['POST'])
@login_required
def delete_application(app_id):
    app = JobApplicationRepository.get_by_id(app_id)
    if not app:
        return jsonify({"error": "Application not found"}), 404
    JobApplicationRepository.delete(app)
    return redirect(url_for('application_bp.applications_page')), 201