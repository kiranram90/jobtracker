from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.users import User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app.dto.user_dto import UserDTO


Bcrypt = Bcrypt()
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400
    
    user_dto = UserDTO.parse_obj(data) 
    if User.query.filter_by(email=user_dto.email).first():
        return jsonify({"error": "User already exists"}), 400   
    hashed_password = Bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=user_dto.email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201
    

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400   
    user_dto = UserDTO.parse_obj(data)
    user = User.query.filter_by(email=user_dto.email).first()
    if user and Bcrypt.check_password_hash(user.password_hash, user_dto.password):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid email or password"}), 401


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200