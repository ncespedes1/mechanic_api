from app.extensions import ma
from app.models import Mechanics


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics

mechanic_schema = MechanicSchema() 
mechanics_schema = MechanicSchema(many=True)
login_schema = MechanicSchema(exclude=['firstname','lastname','salary','address'])