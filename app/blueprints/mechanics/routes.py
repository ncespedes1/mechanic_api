from app.blueprints.mechanics import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema, login_schema
from app.blueprints.service_tickets.schemas import service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Mechanics, db
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required


# POST '/login' : passing in email and password, validated by login_schema
@mechanics_bp.route('/login', methods=['POST'])
@limiter.limit("6 per 10 min")
def login():
    try:
        data = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    mechanic = db.session.query(Mechanics).where(Mechanics.email==data['email']).first()

    if mechanic and check_password_hash(mechanic.password, data['password']):
        token = encode_token(mechanic.id)
        return jsonify({
            "message": f"Welcome {mechanic.firstname} {mechanic.lastname}",
            "token": token
        }), 200
    
    return jsonify("Invalid email or password"), 403

    


@mechanics_bp.route('', methods=['POST'])
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    data['password'] = generate_password_hash(data['password'])

    new_mechanic = Mechanics(**data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route('', methods=['GET'])
def read_mechanics():
    mechanics = db.session.query(Mechanics).all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('<int:mechanic_id>', methods=['GET'])
@token_required
def read_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route('', methods=['DELETE'])
@token_required
def delete_mechanics():
    mechanic_id = request.mechanic_id
    mechanic = db.session.get(Mechanics, mechanic_id)
    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted mechanic {mechanic_id}"}), 200


@mechanics_bp.route('', methods=['PUT'])
@token_required
def update_mechanic():
    mechanic_id = request.mechanic_id
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    mechanic_data['password'] = generate_password_hash(mechanic_data['password'])
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route('/my-tickets', methods=['GET'])
@limiter.limit("12 per hour")
@token_required
def my_tickets():
    mechanic_id = request.mechanic_id
    mechanic = db.session.get(Mechanics, mechanic_id)

    return service_tickets_schema.jsonify(mechanic.service_tickets), 200


# Route to find which (top 3) mechanics work on the most tickets
@mechanics_bp.route('/most-tickets', methods=['GET'])
def most_tickets():
    mechanics = db.session.query(Mechanics).all()

    mechanics.sort(key=lambda mechanic: len(mechanic.service_tickets), reverse=True)

    output = []
    for mechanic in mechanics[:3]:
        mechanic_format = {
            "mechanic": mechanic_schema.dump(mechanic),
            "total_tickets": len(mechanic.service_tickets)
        }
        output.append(mechanic_format)

    return jsonify(output), 200

