from db.db import db_instance

class StoreModel(db_instance.Model):
    __tablename__ = "stores"

    id = db_instance.Column(db_instance.Integer, primary_key=True)
    name = db_instance.Column(db_instance.String(80), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name