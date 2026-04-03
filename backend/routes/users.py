from flask import Blueprint, request, jsonify
from extensions import mongo
from utils.decorators import role_required
from flask_jwt_extended import jwt_required
from bson import ObjectId

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_users():
    users_cursor = mongo.db.users.find({}, {"password_hash": 0}) # exclude password
    users = []
    for user in users_cursor:
        user['_id'] = str(user['_id'])
        users.append(user)
    return jsonify(users), 200

@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    update_fields = {}
    if 'role' in data:
        if data['role'] not in ['viewer', 'analyst', 'admin']:
            return jsonify({"error": "Invalid role"}), 400
        update_fields['role'] = data['role']
        
    if 'is_active' in data:
        update_fields['is_active'] = bool(data['is_active'])

    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        result = mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User updated successfully"}), 200
    except Exception:
        return jsonify({"error": "Invalid user ID"}), 400
