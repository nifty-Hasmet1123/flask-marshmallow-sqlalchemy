from flask.views import MethodView
from flask import Blueprint, request, jsonify
from src.models import Product
from src.schema.ProductSchema import ProductSchema
from src.db.db import db_instance as db
from marshmallow import ValidationError

product_bp = Blueprint("product_bp", __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class ProductView(MethodView):
    # 1 get, post, put, delete
    def post(self):
        data = request.get_json()

        # validate the data using the schema
        # NOTE: in order to remove the try except block create a decorator for it
        try:
            validated_data = product_schema.load(data)
        except ValidationError as e:
            return jsonify({"errors": f"{e.messages}"}), 400
        
        # Create a new product using validated data if there are no errors
        # new_product = Product(
        #     name=validated_data["name"],
        #     description=validated_data.get("description"),
        #     price=validated_data["price"],
        #     qty=validated_data["qty"]
        # )

        # you need to manually handle the logic for duplication marshmallow doesn't provide that!!!
        if self.handle_unique_items(validated_data["name"]):
            return jsonify({ "error": "The data is already existing on the database." }), 400


        # create an instance
        new_product = Product(**validated_data)

        # Add the new product to the database
        db.session.add(new_product)
        db.session.commit()

        # Serialize the product data and return it in the response
        return jsonify({
            "message": "Product created successfully!",
            "product": product_schema.dump(new_product)
        }), 201
    
    def handle_unique_items(self, key_name):
        existing_product = Product.query.filter(
            Product.name == key_name # name is a column within the Product table
        ).first() 

        # returns none if it is not existing
        return existing_product
    
product_view = ProductView.as_view(name="product_api")
product_bp.add_url_rule(
    "/product",
    view_func=product_view,
    methods=["POST"]
)
       