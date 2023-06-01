from bson import ObjectId, json_util
from flask import jsonify, request, json
from app import app, mongo
from models.admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from routes.logging.logger import log


@app.route('/api/admin/get_all', methods=['GET'])
def view_all_admins():
    admins = list(mongo.db.admin.find())
    return jsonify(json.loads(json_util.dumps(admins))), 200


@app.route('/api/admin/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    email = data['email']
    password = data['password']

    existing_admin = mongo.db.admin.find_one({'email': email})
    if existing_admin:
        log(f'Admin with email {email} already exists')
        return jsonify({'message': 'Admin already exists'}), 400

    hashed_password = generate_password_hash(password)
    admin_id = mongo.db.admin.insert_one({
        'email': email,
        'password': hashed_password
    }).inserted_id

    admin = Admin(email, password, admin_id)
    access_token = create_access_token(identity=str(admin.id))
    log(f'User registered with email: {email}')
    return jsonify({'access_token': access_token}), 200


@app.route('/api/admin/login', methods=['POST'])
def login_admin():
    data = request.get_json()
    email = data['email']
    password = data['password']

    existing_admin = mongo.db.admin.find_one({'email': email})
    if not existing_admin:
        return jsonify({'message': 'Admin not found'}), 404

    if check_password_hash(existing_admin['password'], password):
        access_token = create_access_token(identity=str(existing_admin['_id']))
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid password'}), 401


@app.route('/api/admin/update_password', methods=['POST'])
@jwt_required()
def update_admin_password():
    data = request.get_json()
    new_password = data['new_password']

    current_admin_id = get_jwt_identity()
    existing_admin = mongo.db.admin.find_one({'_id': ObjectId(current_admin_id)})
    if not existing_admin:
        log(f'Attempt to update non-existing admin with id: {current_admin_id}')
        return jsonify({'message': 'Admin not found'}), 404

    hashed_password = generate_password_hash(new_password)
    mongo.db.admin.update_one({'_id': ObjectId(current_admin_id)}, {'$set': {'password': hashed_password}})
    log(f'Admin with id {current_admin_id} updated successfully')
    return jsonify({'message': 'Password updated successfully'}), 200


@app.route('/api/admin/delete_account', methods=['DELETE'])
@jwt_required()
def delete_admin_account():
    current_admin_id = get_jwt_identity()
    existing_admin = mongo.db.admin.find_one({'_id': ObjectId(current_admin_id)})
    if not existing_admin:
        log(f'Attempt to delete non-existing admin with id: {current_admin_id}')
        return jsonify({'message': 'Admin not found'}), 404

    mongo.db.admin.delete_one({'_id': ObjectId(current_admin_id)})
    log(f'Admin with id {current_admin_id} deleted successfully')
    return jsonify({'message': 'Admin deleted successfully'}), 200
