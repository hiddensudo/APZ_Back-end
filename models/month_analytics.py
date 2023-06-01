from bson import ObjectId
from app import mongo
from datetime import datetime, timedelta


class Month:
    def __init__(self, user_id, date, month, avg_gas_count, avg_electricity_count, avg_water_count,
                 avg_temperature_count):
        self.id = str(ObjectId())
        self.user_id = user_id
        self.date = date
        self.month = month
        self.avg_gas_count = avg_gas_count
        self.avg_electricity_count = avg_electricity_count
        self.avg_water_count = avg_water_count
        self.avg_temperature_count = avg_temperature_count

    def calculate_monthly_averages(user_id):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        month = end_date.month - 1 if end_date.day < 30 else end_date.month
        year = end_date.year if month != 0 else end_date.year - 1
        month = 12 if month == 0 else month

        pipeline = [
            {'$match': {'user_id': user_id,
                        'date': {'$gte': start_date.strftime('%Y-%m-%d'), '$lte': end_date.strftime('%Y-%m-%d')}}},
            {'$group': {
                '_id': None,
                'avg_gas_count': {'$avg': '$gas_count'},
                'avg_electricity_count': {'$avg': '$electricity_count'},
                'avg_water_count': {'$avg': '$water_count'},
                'avg_day_temperature': {'$avg': '$day_temperature'}
            }}
        ]

        result = mongo.db.day_analytics.aggregate(pipeline)
        result = list(result)

        if result:
            avg_gas_count = round(result[0]['avg_gas_count'], 2)
            avg_electricity_count = round(result[0]['avg_electricity_count'], 2)
            avg_water_count = round(result[0]['avg_water_count'], 2)
            avg_day_temperature = round(result[0]['avg_day_temperature'], 2)

            # Create a new Month object with the calculated averages
            month = Month(
                user_id=user_id,
                date=end_date.strftime('%Y-%m-%d'),
                month=f'{year}-{month:02d}',
                avg_gas_count=avg_gas_count,
                avg_electricity_count=avg_electricity_count,
                avg_water_count=avg_water_count,
                avg_temperature_count=avg_day_temperature
            )

            # Insert the new Month object into the database
            mongo.db.month_analytics.insert_one(month.__dict__)
