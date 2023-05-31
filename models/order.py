class Order:
    def __init__(self, user_id, admin_id, building_id, start_date, end_date, status, _id=None):
        self.user_id = user_id
        self.admin_id = admin_id
        self.building_id = building_id
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self._id = _id
