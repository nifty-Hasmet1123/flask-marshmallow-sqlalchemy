from db.db import db_instance

class ItemModel(db_instance.Model):
    __tablename__ = "items"

    # this is the database validation
    id = db_instance.Column(db_instance.Integer, primary_key=True)
    name = db_instance.Column(db_instance.String(80), unique=True, nullable=False)
    price = db_instance.Column(db_instance.Float(precision=2), unique=False, nullable=False)
    store_id = db_instance.Column(db_instance.Integer, unique=False, nullable=False)

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id