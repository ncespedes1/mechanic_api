from app.blueprints.inventory import inventory_bp
from .schemas import inventory_schema, inventory_many_schema, inv_desc_schema, inv_desc_many_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Inventory, Inventory_descriptions, db
from app.extensions import limiter, cache
from sqlalchemy import select


@inventory_bp.route('', methods=['POST'])
def create_inventory():
    try:
        data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    

    new_inventory = Inventory(**data)
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201


@inventory_bp.route('', methods=['GET'])
# @cache.cached(timeout=30)
def read_inventory_many():
        inventory_many = db.session.query(Inventory).all()
        return inventory_many_schema.jsonify(inventory_many), 200


@inventory_bp.route('<int:inventory_id>', methods=['GET'])
def read_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    return inventory_schema.jsonify(inventory), 200


@inventory_bp.route('<int:inventory_id>', methods=['DELETE'])
def delete_inventory_many(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    db.session.delete(inventory)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted Inventory {inventory_id}"}), 200


@inventory_bp.route('<int:inventory_id>', methods=['PUT'])
def update_customer(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify({"message": "Inventory not found"}), 404
    
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in inventory_data.items():
        setattr(inventory, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200


#-----------------------inv_desc-------------------------

@inventory_bp.route('/descriptions', methods=['POST'])
def create_inventory_desc():
    try:
        data = inv_desc_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    

    new_inventory_desc = Inventory_descriptions(**data)
    db.session.add(new_inventory_desc)
    db.session.commit()
    return inv_desc_schema.jsonify(new_inventory_desc), 201


