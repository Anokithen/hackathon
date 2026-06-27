from flask import jsonify, request

from app.extensions import db
from app.models.customers_model import customers


def _validate_customer_payload(data, customer_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    name = data.get("name")
    if name is None or str(name).strip() == "":
        errors.append("Name is required.")
    elif str(name).strip():
        q = customers.query.filter(customers.name == str(name).strip())
        if customer_id:
            q = q.filter(customers.id != customer_id)
        if q.first():
            errors.append("Customer name already exists.")

    fee = data.get("customer_fee")
    if fee is None:
        errors.append("customer_fee is required.")
    else:
        try:
            fee_val = float(fee)
            if fee_val <= 0:
                errors.append("customer_fee must be a positive number.")
        except (TypeError, ValueError):
            errors.append("customer_fee must be a positive number.")

    duration = data.get("duration_months")
    if duration is None:
        errors.append("duration_months is required.")
    else:
        try:
            dur_val = int(duration)
            if dur_val <= 0:
                errors.append("duration_months must be a positive integer.")
        except (TypeError, ValueError):
            errors.append("duration_months must be a positive integer.")

    return errors


def create_customer():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_customer_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        customer = customers(
            name=data.get("name").strip(),
            customer_fee=float(data.get("customer_fee")),
            duration_months=int(data.get("duration_months")),
            description=data.get("description"),
            is_available=data.get("is_available", True),
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({"message": "Customer created successfully.", "customer": customer.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_customers():
    customers_list = customers.query.all()
    return jsonify({"customers": [c.to_dict() for c in customers_list]}), 200


def get_customer(customer_id):
    customer = customers.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    return jsonify({"customer": customer.to_dict()}), 200


def update_customer(customer_id):
    customer = customers.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_customer_payload(data, customer_id=customer_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        customer.name = data.get("name").strip()
        customer.customer_fee = float(data.get("customer_fee"))
        customer.duration_months = int(data.get("duration_months"))
        if "description" in data:
            customer.description = data.get("description")
        if "is_available" in data:
            customer.is_available = bool(data.get("is_available"))
        db.session.commit()
        return jsonify({"message": "Customer updated successfully.", "customer": customer.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_customer(customer_id):
    customer = customers.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
