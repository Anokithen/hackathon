from flask import Blueprint

from app.controllers.customers_controller import (
    create_customer,
    delete_customer,
    get_customer,
    get_customers,
    update_customer,
)

customers_bp = Blueprint("customers", __name__)

customers_bp.route("/", methods=["GET"])(get_customers)
customers_bp.route("/<int:customer_id>", methods=["GET"])(get_customer)
customers_bp.route("/", methods=["POST"])(create_customer)
customers_bp.route("/<int:customer_id>", methods=["PUT"])(update_customer)
customers_bp.route("/<int:customer_id>", methods=["DELETE"])(delete_customer)