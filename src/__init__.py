from flask import Flask
from src.db.db import db_instance
from src.db.ma import ma
from sqlalchemy.exc import OperationalError

def create_app():
    # make sure to import the models here 
    from src.models import Product

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/pyqt-server"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    initiate_database_connection(app)
    initiate_marshmallow_app(app)
    register_blueprint(app)

    return app

def initiate_database_connection(app):
    db_instance.init_app(app)

    with app.app_context():
        try:
            with db_instance.engine.connect() as conn:
                print(f"Connected to the database: {conn}")
            db_instance.create_all()
        except OperationalError as e:
            print(f"Failed to connect to the database: {e}")

def initiate_marshmallow_app(app):
    ma.init_app(app)

def register_blueprint(app):
    from src.routes.my_route import product_bp

    app.register_blueprint(product_bp, url_prefix="/")