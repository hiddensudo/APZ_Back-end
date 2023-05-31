from app import mongo, app
from flask import request, jsonify
from models.month_analytics import Month
from datetime import datetime, timedelta


@app.route('/api/monthly/averages', methods=['POST'])
def calculate_averages_route():
    data = request.get_json()
    user_id = data['user_id']

    Month.calculate_monthly_averages(user_id)

    return jsonify({'message': 'Monthly averages successfully calculated'}), 201
