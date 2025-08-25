from init import db
from marshmallow import fields

class AppointmentService(db.Model):
    __tablename__ = "appointment_services"

    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), primary_key=True)

    # Relationships
    appointment = db.relationship("Appointment", back_populates="appointmentservices")
    service = db.relationship("Service", back_populates="appointmentservices")