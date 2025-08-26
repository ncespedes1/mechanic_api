from app.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, db
from app.extensions import cache
from sqlalchemy import select


@customers_bp.route('', methods=['POST'])
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    

    new_customer = Customers(**data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


@customers_bp.route('', methods=['GET'])
@cache.cached(timeout=30)
def read_customers():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customers)
        service_tickets = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(service_tickets), 200
    except:
        customers = db.session.query(Customers).all()
        return customers_schema.jsonify(customers), 200


@customers_bp.route('<int:customer_id>', methods=['GET'])
def read_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    return customer_schema.jsonify(customer), 200


@customers_bp.route('/search-email', methods=['GET'])
def search_email():
    email = request.args.get('email')
    
    customer = db.session.query(Customers).where(Customers.email==email).first()
    return customer_schema.jsonify(customer), 200


@customers_bp.route('<int:customer_id>', methods=['DELETE'])
def delete_customers(customer_id):
    customer = db.session.get(Customers, customer_id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted customer {customer_id}"}), 200


@customers_bp.route('<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)

    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


