from app.extensions import ma
from app.models import Service_tickets


class Service_ticketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_tickets

service_ticket_schema = Service_ticketSchema() 
service_tickets_schema = Service_ticketSchema(many=True)