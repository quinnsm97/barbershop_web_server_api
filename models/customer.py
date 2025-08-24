from init import db

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relationship to appointments
    appointments = db.relationship("Appointment", back_populates="customer", cascade="all, delete")

