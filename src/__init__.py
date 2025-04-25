from flask import Flask
from src.db.db import db_instance
from src.db.ma import ma
from sqlalchemy.exc import OperationalError
import os

def create_app():
    # make sure to import the models here 
    from src.models import Product

    template_path = find_template_folder()

    app = Flask(__name__, template_folder=template_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/pyqt-server"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    initiate_database_connection(app)
    initiate_marshmallow_app(app)
    register_blueprint(app)

    return app

def find_template_folder():
    base_dir = os.getcwd()
    template_folder_path = os.path.join(base_dir, "src", "templates")
    return template_folder_path

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
    from src.routes.with_jinja_route import sample_bp
    from src.routes.qr_code_route import qrcode_bp

    # app.register_blueprint(product_bp, url_prefix="/")
    app.register_blueprint(sample_bp)
    app.register_blueprint(qrcode_bp)