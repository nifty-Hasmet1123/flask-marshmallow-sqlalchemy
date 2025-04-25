from src.db.db import db_instance

class Product(db_instance.Model):
    __tablename__ = "product"

    id = db_instance.Column(db_instance.Integer, primary_key=True)
    name = db_instance.Column(db_instance.String(100), unique=True, nullable=False)
    description = db_instance.Column(db_instance.String(100), nullable=True)
    price = db_instance.Column(db_instance.Float(precision=2), nullable=False)
    qty = db_instance.Column(db_instance.Integer, nullable=False)

    def __init__(self, name, price, qty, description=None):
        self.name = name
        self.price = price
        self.qty = qty
        self.description = description

