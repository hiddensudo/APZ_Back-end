from bson import ObjectId, json_util
from flask import jsonify, request, redirect, render_template, session, url_for, json
from app import app, mongo
from models.admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from bson.json_util import dumps


@app.route('/api/order/get_all', methods=['GET'])
@jwt_required()
def get_all_orders():
    current_user_id = get_jwt_identity()
    existing_user = mongo.db.user.find_one({'_id': ObjectId(current_user_id)})
    if not existing_user:
        return jsonify(json.loads(json_util.dumps(existing_user))), 200

    orders = list(mongo.db.order.find({'user_id': current_user_id}))
    return jsonify(json.loads(json_util.dumps(orders))), 200


@app.route('/api/order/add', methods=['POST'])
def add_order():
    data = request.get_json()
    user_id = data['user_id']
    building_id = data['building_id']
    start_date = data['start_date']
    end_date = data['end_date']
    status = data['status']

    existing_user = mongo.db.user.find_one({'_id': ObjectId(user_id)})
    if not existing_user:
        return jsonify({'message': 'User not found'}), 404

    building = mongo.db.building.find_one({'_id': ObjectId(building_id)})
    if not building:
        return jsonify({'message': 'Building not found'}), 404

    admin_id = existing_user['_id']

    order_id = mongo.db.order.insert_one({
        'user_id': user_id,
        'admin_id': admin_id,
        'building_id': building_id,
        'start_date': start_date,
        'end_date': end_date,
        'status': status
    }).inserted_id

    return jsonify({'message': 'Order successfully added'}), 201


@app.route('/api/order/update', methods=['PUT'])
def update_order():
    data = request.get_json()
    order_id = data['order_id']
    start_date = data['start_date']
    end_date = data['end_date']
    status = data['status']

    existing_order = mongo.db.order.find_one({'_id': ObjectId(order_id)})
    if not existing_order:
        return jsonify({'message': 'Order not found'}), 404

    mongo.db.order.update_one(
        {'_id': ObjectId(order_id)},
        {'$set': {
            'start_date': start_date,
            'end_date': end_date,
            'status': status
        }}
    )

    return jsonify({'message': 'Order successfully updated'}), 200


@app.route('/api/order/delete', methods=['DELETE'])
def delete_order():
    data = request.get_json()
    order_id = data['order_id']

    existing_order = mongo.db.order.find_one({'_id': ObjectId(order_id)})
    if not existing_order:
        return jsonify({'message': 'Order not found'}), 404

    mongo.db.order.delete_one({'_id': ObjectId(order_id)})

    return jsonify({'message': 'Order successfully deleted'}), 200
