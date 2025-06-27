from flask import Blueprint, request, jsonify
from app import db
from app.models.users import User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app.dto.user_dto import UserDTO


Bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400
    user_dto = UserDTO.parse_obj(data)
    