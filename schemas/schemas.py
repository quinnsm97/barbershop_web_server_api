from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from models.customer import Customer
from models.staff import Staff
from models.appointment import Appointment

class CustomerSchema(SQLAlchemyAutoSchema):
    appointments = fields.Nested("AppointmentSchema", many=True, exclude=("customer",))
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id", "first_name", "last_name", "email", "phone", "appointments")
        ordered = True

# Single entry
customer_schema = CustomerSchema()
# Multiple entries
customer_schemas = CustomerSchema(many=True)

class StaffSchema(SQLAlchemyAutoSchema):
    appointments = fields.Nested("AppointmentSchema", many=True, exclude=("staff",))
    class Meta:
        model = Staff
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id", "first_name", "last_name", "role", "specialty", "appointments")
        ordered = True

# Single entry
staff_schema = StaffSchema()
# Multiple entries
staff_schemas = StaffSchema(many=True)

class AppointmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        load_instance = True
        include_fk = True
        include_relationships = True
    customer = fields.Nested("CustomerSchema", only=("id", "first_name", "last_name"))
    staff = fields.Nested("StaffSchema", only=("id", "first_name", "last_name", "specialty"))

# Single entry
appointment_schema = AppointmentSchema()
# Multiple entries
appointment_schemas = AppointmentSchema(many=True) 