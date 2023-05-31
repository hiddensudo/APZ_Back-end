from bson import ObjectId


class Order:
    def __init__(self, user_email, admin_email, status, start_date, end_date):
        self.user_email = user_email
        self.admin_email = admin_email
        self.building_id = str(ObjectId())
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
