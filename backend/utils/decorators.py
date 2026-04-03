from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from extensions import mongo
from bson import ObjectId

# Custom wrapper to enforce our Role-Based Access Control (RBAC) securely on any API route
def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            try:
                user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            except Exception:
                return jsonify({"error": "Invalid user ID Format"}), 400
                
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            if not user.get("is_active", True):
                return jsonify({"error": "Account is inactive"}), 403

            if user.get("role") not in roles:
                return jsonify({"error": f"Role restricted. Requires one of: {roles}"}), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper
