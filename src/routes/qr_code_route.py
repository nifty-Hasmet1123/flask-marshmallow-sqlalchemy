from flask import render_template, jsonify, Blueprint, request, url_for
from flask.views import MethodView
from io import BytesIO
import qrcode
import uuid
import json
import base64
import logging

qrcode_bp = Blueprint("qrcode_bp", __name__, url_prefix="/qr")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_data = {}
class QRCode(MethodView):
    def get(self):
        # adding the qr_image on view to make the condition in the qr_code_form.html to not display the qr code on reload
        return render_template("qr_code_form.html", qr_image=None)
    def post(self):
        # first_name = request.form.get("first_name")
        # last_name = request.form.get("last_name")
        # email = request.form.get("email")
        qr_image = self.generate_qr_code(**request.form)

        # return jsonify({
        #     "first_name": first_name,
        #     "last_name": last_name,
        #     "email": email
        # })
        # return render_template("qr_code_form.html", data={
        #     "first_name": first_name,
        #     "last_name": last_name,
        #     "email": email
        # })
        return render_template("qr_code_form.html", qr_image=qr_image)
    
    def generate_qr_code(self, **kwargs):
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        email = kwargs.get("email")

        token = str(uuid.uuid4())
        # should be store in a database etc.
        user_data[token] = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }

        # generate a qr code containing the URL with the token 
        qr_url = f"http://192.168.100.4:5000{url_for("qrcode_bp.view_user_data", token=token)}"
        logger.info(f"\n***\n{qr_url}\n***")

        buffer= BytesIO()
        image = qrcode.make(qr_url)
        image.save(buffer, format="PNG")
        qr_img_base_64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return qr_img_base_64
    
@qrcode_bp.route("/user_data/<token>", methods=["GET"])
def view_user_data(token):
    user = user_data.get(token)

    if user:
        return render_template("user_data.html", user=user)
    else:
        return "Data not found", 404
    
qrcode_view = QRCode.as_view("qr_code_view")
qrcode_bp.add_url_rule(
    "/user",
    view_func=qrcode_view,
    methods=["GET"]
)
qrcode_bp.add_url_rule(
    "/user",
    view_func=qrcode_view,
    methods=["POST"]
)

