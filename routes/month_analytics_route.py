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


@app.route('/api/monthly/averages/get', methods=['GET'])
def get_monthly_averages():
    results = mongo.db.month_analytics.find()
    data = []
    for result in results:
        data.append({
            "date": result["date"],
            "month": result["month"],
            "avg_gas_count": result["avg_gas_count"],
            "avg_electricity_count": result["avg_electricity_count"],
            "avg_water_count": result["avg_water_count"],
            "avg_temperature_count": result["avg_temperature_count"]
        })
    return jsonify(data), 200
