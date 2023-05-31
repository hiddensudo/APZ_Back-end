from bson import ObjectId, json_util
from flask import jsonify, request, redirect, render_template, session, url_for, json
from app import app, mongo
from models.building import Building
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from bson.json_util import dumps


@app.route('/api/buildings/get_all', methods=['GET'])
def view_all_buildings():
    buildings = list(mongo.db.building.find())
    return jsonify(json.loads(json_util.dumps(buildings))), 200


@app.route('/api/buildings/add', methods=['POST'])
@jwt_required()
def add_building():
    data = request.get_json()
    address = data['address']

    current_user_id = get_jwt_identity()
    existing_user = mongo.db.user.find_one({'_id': ObjectId(current_user_id)})
    if not existing_user:
        return jsonify({'message': 'User not found'}), 404

    building_id = mongo.db.building.insert_one({
        'user_id': current_user_id,
        'address': address
    }).inserted_id

    return jsonify({'message': 'building add successfully'}), 201


@app.route('/api/buildings/update', methods=['PUT'])
@jwt_required()
def update_building():
    data = request.get_json()
    building_id = data['building_id']
    address = data['address']

    current_user_id = get_jwt_identity()
    existing_user = mongo.db.user.find_one({'_id': ObjectId(current_user_id)})
    if not existing_user:
        return jsonify({'message': 'User not found'}), 404

    mongo.db.building.update_one(
        {'_id': ObjectId(building_id)},
        {'$set': {'address': address}}
    )

    return jsonify({'message': 'building update successfully'}), 200


@app.route('/api/buildings/delete', methods=['DELETE'])
@jwt_required()
def delete_building():
    data = request.get_json()
    building_id = data['building_id']

    current_user_id = get_jwt_identity()
    existing_user = mongo.db.user.find_one({'_id': ObjectId(current_user_id)})
    if not existing_user:
        return jsonify({'message': 'User not found'}), 404

    mongo.db.building.delete_one({'_id': ObjectId(building_id)})

    return jsonify({'message': 'building delete successfully'}), 200
