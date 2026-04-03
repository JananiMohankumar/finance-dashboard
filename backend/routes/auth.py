from flask import Blueprint, request, jsonify
from extensions import bcrypt, jwt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

from extensions import mongo

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = mongo.db.users.find_one({"email": data['email']})
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 409

    # Securely hash the plain text password so it's not stored raw in our DB
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    count = mongo.db.users.count_documents({})
    
    # Logic to ensure we don't get locked out: the very first user to register gets Admin rights
    role = data.get('role', 'viewer')
    if count == 0:
        role = 'admin'

    new_user = {
        "username": data['username'],
        "email": data['email'],
        "password_hash": hashed_pw,
        "role": role,
        "is_active": True
    }

    result = mongo.db.users.insert_one(new_user)
    return jsonify({"message": "User created successfully", "id": str(result.inserted_id)}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    user = mongo.db.users.find_one({"email": data['email']})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.check_password_hash(user['password_hash'], data['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.get('is_active', True):
        return jsonify({"error": "Account is disabled"}), 403

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": str(user['_id']),
            "username": user['username'],
            "email": user['email'],
            "role": user['role']
        }
    }), 200
