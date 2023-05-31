from bson import ObjectId


class Month:
    def __init__(self, client_email, date, avg_gas_count, avg_electricity_count, avg_water_count,
                 avg_temperature_count):
        self.id = str(ObjectId())
        self.client_email = client_email
        self.date = date
        self.gas_count = avg_gas_count
        self.electricity_count = avg_electricity_count
        self.water_count = avg_water_count
        self.day_temperature = avg_temperature_count
