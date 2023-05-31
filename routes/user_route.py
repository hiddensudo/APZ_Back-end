from bson import ObjectId
from flask import jsonify, request, redirect, render_template, session, url_for
from app import app, mongo
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from bson.json_util import dumps


@app.route('/api/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

    existing_client = mongo.db.user.find_one({'email': email})
    if existing_client:
        return jsonify({'message': 'Client already exists'}), 400

    hashed_password = generate_password_hash(password)
    client_id = mongo.db.user.insert_one({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': hashed_password
    }).inserted_id

    client = User(first_name, last_name, email, password, client_id)
    access_token = create_access_token(identity=str(client.id))
    return jsonify({'access_token': access_token}), 200
