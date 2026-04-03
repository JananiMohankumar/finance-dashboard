from flask import Blueprint, request, jsonify
from extensions import mongo
from utils.decorators import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime

records_bp = Blueprint('records', __name__)

@records_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analyst'])
def get_records():
    query = {}
    record_type = request.args.get('type')
    category = request.args.get('category')
    
    if record_type:
        query['type'] = record_type
    if category:
        query['category'] = category

    records_cursor = mongo.db.records.find(query).sort('date', -1)
    
    records = []
    for record in records_cursor:
        record['_id'] = str(record['_id'])
        record['created_by'] = str(record.get('created_by'))
        records.append(record)
        
    return jsonify(records), 200

@records_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_record():
    data = request.get_json()
    required = ['amount', 'type', 'category', 'date']
    if not data or not all(k in data for k in required):
        return jsonify({"error": f"Missing one or more required fields: {required}"}), 400

    if data['type'] not in ['income', 'expense']:
        return jsonify({"error": "Type must be 'income' or 'expense'"}), 400

    try:
        amount = float(data['amount'])
        date_obj = datetime.fromisoformat(data['date'].replace("Z", "+00:00"))
    except ValueError:
        return jsonify({"error": "Invalid amount or date format (use ISO format for date)"}), 400

    user_id = get_jwt_identity()

    new_record = {
        "amount": amount,
        "type": data['type'],
        "category": data['category'],
        "date": date_obj,
        "notes": data.get('notes', ''),
        "created_by": ObjectId(user_id)
    }

    result = mongo.db.records.insert_one(new_record)
    return jsonify({"message": "Record created", "id": str(result.inserted_id)}), 201

@records_bp.route('/<record_id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_record(record_id):
    try:
        result = mongo.db.records.delete_one({"_id": ObjectId(record_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Record not found"}), 404
        return jsonify({"message": "Record deleted successfully"}), 200
    except Exception:
        return jsonify({"error": "Invalid record ID"}), 400
        
@records_bp.route('/<record_id>', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def update_record(record_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    update_fields = {}
    if 'amount' in data:
        try:
            update_fields['amount'] = float(data['amount'])
        except ValueError:
            return jsonify({"error": "Invalid amount"}), 400
    if 'type' in data:
        if data['type'] not in ['income', 'expense']:
            return jsonify({"error": "Invalid type"}), 400
        update_fields['type'] = data['type']
    if 'category' in data:
        update_fields['category'] = data['category']
    if 'notes' in data:
        update_fields['notes'] = data['notes']
    if 'date' in data:
        try:
            update_fields['date'] = datetime.fromisoformat(data['date'].replace("Z", "+00:00"))
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400

    try:
        result = mongo.db.records.update_one({"_id": ObjectId(record_id)}, {"$set": update_fields})
        if result.matched_count == 0:
            return jsonify({"error": "Record not found"}), 404
        return jsonify({"message": "Record updated successfully"}), 200
    except Exception:
        return jsonify({"error": "Invalid record ID"}), 400
