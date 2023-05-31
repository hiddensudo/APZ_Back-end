from bson import ObjectId, json_util
from flask import jsonify, request, redirect, render_template, session, url_for, json
from app import app, mongo
from models.admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from bson.json_util import dumps
from datetime import datetime


@app.route('/api/daily/get_all', methods=['GET'])
def get_all_days():
    data = request.args
    user_id = data['user_id']

    days = list(mongo.db.day_analytics.find({'user_id': user_id}))
    return jsonify(json.loads(json_util.dumps(days))), 200


@app.route('/api/daily/add', methods=['POST'])
def add_day():
    data = request.get_json()
    user_id = data['user_id']
    gas_count = data['gas_count']
    electricity_count = data['electricity_count']
    water_count = data['water_count']
    day_temperature = data['day_temperature']

    date = datetime.now().strftime('%Y-%m-%d')

    existing_day = mongo.db.day_analytics.find_one({'user_id': user_id, 'date': date})
    if existing_day:
        return jsonify({'message': 'Data for today has already been added'}), 400

    day_id = mongo.db.day_analytics.insert_one({
        'user_id': user_id,
        'date': date,
        'gas_count': gas_count,
        'electricity_count': electricity_count,
        'water_count': water_count,
        'day_temperature': day_temperature
    }).inserted_id

    return jsonify({'message': 'Daily data successfully added'}), 201


@app.route('/api/daily/delete', methods=['DELETE'])
def delete_day():
    data = request.args
    day_id = data['day_id']

    existing_day = mongo.db.day_analytics.find_one({'_id': ObjectId(day_id)})
    if not existing_day:
        return jsonify({'message': 'Data not found'}), 404

    mongo.db.day_analytics.delete_one({'_id': ObjectId(day_id)})

    return jsonify({'message': 'Data successfully deleted'}), 200
