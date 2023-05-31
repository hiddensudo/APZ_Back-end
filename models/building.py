class Building:
    def __init__(self, user_id, address, _id=None):
        self.user_id = user_id
        self.address = address
        self._id = _id

    @property
    def id(self):
        return self._id
