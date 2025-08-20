from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Staff(db.Model):
    __tablename__ = "staff"
    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    specialty = db.Column(db.String(100))

class StaffSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Staff
        load_instance = True

# Single entry
staff_schema = StaffSchema()
# Multiple entries
staff_schemas = StaffSchema(many=True)