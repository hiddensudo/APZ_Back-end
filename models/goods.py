class Goods:
    def __init__(self, name, description, price, _id=None):
        self.name = name
        self.description = description
        self.price = price
        self._id = _id

    @property
    def id(self):
        return self._id
