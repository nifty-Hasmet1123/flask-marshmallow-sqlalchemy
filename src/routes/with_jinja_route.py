from flask.views import MethodView
from flask import Blueprint, render_template, jsonify
from src.models import Product
import logging

sample_bp = Blueprint("sample_bp", __name__, url_prefix="/jinja")

class MyIndex(MethodView):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def get(self):
        # now fetch the data here from the database if ever
        return render_template("index.html")
    
    # no need to use add_url_rule since this is a static method
    @staticmethod
    @sample_bp.route("/get_products", methods=["GET"], endpoint="get_products") # endpoint for jinja template
    def get_products():
        # get the Product model from the product.py then from there query your result
        data = Product.query.all()

        # MyIndex.logger.info(f"\n\n***Data: {data}\n***")
        # MyIndex.logger.info(f"\n\n***Data: {data[0].to_dict()}\n***")
        
        # add a to_dict method on the Product Model
        data = [d.to_dict() for d in data]

        # return jsonify({
        #     "Info": "success",
        #     "data": data
        # }), 200

        return render_template("product.html", products=data)

            
my_view = MyIndex.as_view(name="index_view") # like an endpoint in jinja template
sample_bp.add_url_rule(
    "/home",
    view_func=my_view,
    methods=["GET"]
)