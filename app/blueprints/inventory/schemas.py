from app.extensions import ma
from app.models import Inventory, Inventory_descriptions


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        include_fk = True

inventory_schema = InventorySchema() 
inventory_many_schema = InventorySchema(many=True)



class InventoryDescriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory_descriptions

inv_desc_schema = InventoryDescriptionSchema()
inv_desc_many_schema = InventoryDescriptionSchema(many=True)