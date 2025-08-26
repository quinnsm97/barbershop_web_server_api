from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from models.customer import Customer
from models.staff import Staff
from models.appointment import Appointment
from models.service import Service
from models.appointment_service import AppointmentService

class CustomerSchema(SQLAlchemyAutoSchema):
    appointments = fields.Nested("AppointmentSchema", many=True, only=("id", "appointment_datetime", "services"))
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
    appointments = fields.Nested("AppointmentSchema", many=True, only=("id", "appointment_datetime", "services"))
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

class ServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id", "name", "price", "duration_minutes", "description")
        ordered = True

# Single entry
service_schema = ServiceSchema()
# Multiple entries
service_schemas = ServiceSchema(many=True)

class AppointmentSchema(SQLAlchemyAutoSchema):
    services = fields.Nested("ServiceSchema", many=True, exclude=("id",))
    class Meta:
        model = Appointment
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "appointment_datetime", "status", "customer", "staff", "services")
    customer = fields.Nested("CustomerSchema", only=("first_name", "last_name"))
    staff = fields.Nested("StaffSchema", only=("first_name", "last_name", "specialty"))

# Single entry
appointment_schema = AppointmentSchema()
# Multiple entries
appointment_schemas = AppointmentSchema(many=True)

class AppointmentServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AppointmentService
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("appointment_id", "service_id")
        ordered = True

appointment_service_schema = AppointmentServiceSchema()
appointment_service_schemas = AppointmentServiceSchema(many=True)