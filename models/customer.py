from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False, unique=True)

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

# Single entry
customer_schema = CustomerSchema()
# Multiple entries
customer_schemas = CustomerSchema(many=True)