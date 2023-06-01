from bson import ObjectId
from flask import jsonify, request, json
from app import app, mongo
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from bson import json_util
from logging.logger import log


@app.route('/api/user/get_all', methods=['GET'])
def get_all_users():
    users = list(mongo.db.user.find())
    return jsonify(json.loads(json_util.dumps(users))), 200


@app.route('/api/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

    existing_user = mongo.db.user.find_one({'email': email})
    if existing_user:
        log(f'Attempt to register user with existing email: {email}')
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    user_id = mongo.db.user.insert_one({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': hashed_password
    }).inserted_id

    user = User(first_name, last_name, email, password, user_id)
    access_token = create_access_token(identity=str(user.id))
    log(f'User registered with email: {email}')
    return jsonify({'access_token': access_token}), 200


@app.route('/api/user/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']

    existing_user = mongo.db.user.find_one({'email': email})
    if not existing_user:
        return jsonify({'message': 'User not found'}), 404

    if check_password_hash(existing_user['password'], password):
        access_token = create_access_token(identity=str(existing_user['_id']))
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid password'}), 401


@app.route('/api/user/update_password', methods=['POST'])
@jwt_required()
def update_password():
    data = request.get_json()
    new_password = data['new_password']

    current_user_id = get_jwt_identity()
    existing_user = mongo.db.user.find_one({'_id': ObjectId(current_user_id)})
    if not existing_user:
        log(f'Attempt to update non-existing user with id: {current_user_id}')
        return jsonify({'message': 'User not found'}), 404

    hashed_password = generate_password_hash(new_password)
    mongo.db.user.update_one({'_id': ObjectId(current_user_id)}, {'$set': {'password': hashed_password}})
    log(f'User with id {current_user_id} updated successfully')
    return jsonify({'message': 'Password updated successfully'}), 200


@app.route('/api/user/delete_account', methods=['DELETE'])
@jwt_required()
def delete_account():
    current_user_id = get_jwt_identity()
    existing_user = mongo.db.user.find_one({'_id': ObjectId(current_user_id)})
    if not existing_user:
        log(f'Attempt to delete non-existing user with id: {current_user_id}')
        return jsonify({'message': 'User not found'}), 404

    mongo.db.user.delete_one({'_id': ObjectId(current_user_id)})
    log(f'User with id {current_user_id} deleted successfully')
    return jsonify({'message': 'Account deleted successfully'}), 200
