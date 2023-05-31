class Admin:
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = _id

    @property
    def id(self):
        return self._id
