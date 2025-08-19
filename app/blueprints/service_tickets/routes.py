from app.blueprints.service_tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Service_tickets, Mechanics, db
from app.extensions import limiter, cache


@service_tickets_bp.route('', methods=['POST'])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    

    new_service_ticket = Service_tickets(**data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201


@service_tickets_bp.route('', methods=['GET'])
@cache.cached(timeout=30)
def read_service_tickets():
    service_tickets = db.session.query(Service_tickets).all()
    return service_tickets_schema.jsonify(service_tickets), 200


@service_tickets_bp.route('<int:service_ticket_id>', methods=['GET'])
def read_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_tickets, service_ticket_id)
    return service_ticket_schema.jsonify(service_ticket), 200


@service_tickets_bp.route('<int:service_ticket_id>', methods=['DELETE'])
def delete_service_tickets(service_ticket_id):
    service_ticket = db.session.get(Service_tickets, service_ticket_id)
    db.session.delete(service_ticket)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted Service Ticket {service_ticket_id}"}), 200


@service_tickets_bp.route('<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
@limiter.limit("2 per day")
def remove_mechanic(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_tickets, service_ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not service_ticket:
        return jsonify({"message": "Service ticket not found"}), 404
    
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    if mechanic not in service_ticket.mechanics:
        return jsonify({"message": f"Mechanic {mechanic.firstname} {mechanic.lastname} not previously assigned to Service Ticket {service_ticket_id}"}), 400
        
    service_ticket.mechanics.remove(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200


@service_tickets_bp.route('<int:service_ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_tickets, service_ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    if mechanic in service_ticket.mechanics:
        return jsonify({"message": f"Mechanic {mechanic.firstname} {mechanic.lastname} already assigned to Service Ticket {service_ticket_id}"}), 400
        
    service_ticket.mechanics.append(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200


