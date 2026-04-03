from flask import Blueprint, jsonify
from extensions import mongo
from utils.decorators import role_required
from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():

    # I used MongoDB aggregation pipelines here instead of bringing everything into Python. 
    # This acts like a 'GROUP BY' in SQL and is much faster for the dashboard stats.
    pipeline_totals = [
        {"$group": {
            "_id": "$type",
            "totalAmount": {"$sum": "$amount"}
        }}
    ]
    
    totals_cursor = mongo.db.records.aggregate(pipeline_totals)
    
    total_income = 0
    total_expense = 0
    
    for t in totals_cursor:
        if t['_id'] == 'income':
            total_income = t['totalAmount']
        elif t['_id'] == 'expense':
            total_expense = t['totalAmount']
            
    net_balance = total_income - total_expense
    
    pipeline_categories = [
        {"$group": {
            "_id": {"type": "$type", "category": "$category"},
            "totalAmount": {"$sum": "$amount"}
        }}
    ]
    categories_cursor = mongo.db.records.aggregate(pipeline_categories)
    
    categories = []
    for c in categories_cursor:
        categories.append({
            "type": c['_id']['type'],
            "category": c['_id']['category'],
            "amount": c['totalAmount']
        })

    recent_cursor = mongo.db.records.find().sort('date', -1).limit(5)
    recent_activity = []
    for r in recent_cursor:
        recent_activity.append({
            "id": str(r['_id']),
            "amount": r['amount'],
            "type": r['type'],
            "category": r['category'],
            "date": r['date'].isoformat()
        })

    return jsonify({
        "summary": {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance
        },
        "by_category": categories,
        "recent_activity": recent_activity
    }), 200
