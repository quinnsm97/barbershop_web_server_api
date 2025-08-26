from init import db

class Service(db.Model):
     __tablename__ = "services"
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(50), unique=True, nullable=False)
     price = db.Column(db.Float, nullable=False)
     duration_minutes = db.Column(db.Integer, default=30)
     description = db.Column(db.String(500))

     # Relationships
     appointmentservices = db.relationship("AppointmentService", back_populates="service")
     appointments = db.relationship("Appointment", secondary="appointment_services", back_populates="services")