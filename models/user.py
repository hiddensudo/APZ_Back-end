class User:
    def __init__(self, first_name, last_name, email, password, _id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self._id = _id

    @property
    def id(self):
        return self._id
