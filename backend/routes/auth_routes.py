from flask import Blueprint, request, jsonify
from models.user import User, db, bcrypt
from flask_jwt_extended import create_access_token

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {username} created successfully"}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Create a token that expires in 1 day (you can change this)
        access_token = create_access_token(identity=user.id) 
        return jsonify(access_token=access_token)
    else:
        return jsonify({"error": "Invalid username or password"}), 401