from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.users import User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app.dto.user_dto import UserDTO
from flask import render_template, redirect, url_for

bcrypt = Bcrypt()
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.form or request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400
    
    user_dto = UserDTO.parse_obj(data) 
    
    if User.query.filter_by(email=user_dto.email).first():
        
        return jsonify({"error": "User already exists"}), 400 
        
      
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=user_dto.email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    if request.form:
        return redirect(url_for('auth_bp.login_form'))
    return jsonify({"message": "User registered successfully"}), 201
    

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form or request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400   
    user_dto = UserDTO.parse_obj(data)
    user = User.query.filter_by(email=user_dto.email).first()
    if user and bcrypt.check_password_hash(user.password_hash, user_dto.password):
        login_user(user)
        if request.form:
            return redirect(url_for('application_bp.applications_page'))
        return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"error": "Invalid email or password"}), 401


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login_form'))