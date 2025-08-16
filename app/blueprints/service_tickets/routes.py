from app.blueprints.service_tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Service_tickets, db


@service_tickets_bp('', methods=['POST'])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_tickets(**data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201


@service_tickets_bp('', methods=['GET'])
def read_service_tickets():
    service_tickets = db.session.query(Service_tickets).all()
    return service_ticket_schema.jsonify(service_tickets), 200

@service_tickets_bp('<int:service_ticket_id>', methods=['GET'])
def read_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_tickets, service_ticket_id)
    return service_ticket_schema.jsonify(service_ticket), 200


@service_tickets_bp('<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_tickets, service_ticket_id)
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted service_ticket {service_ticket_id}"}), 200


@service_tickets_bp.route('<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_tickets, service_ticket_id)

    if not service_ticket:
        return jsonify({"message": "Service ticket not found"}), 404
    
    try:
        service_ticket_data = service_ticket_schema.load(request.json) 
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in service_ticket_data.items():
        setattr(service_ticket, key, value) 

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200