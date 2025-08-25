from init import db
from marshmallow import fields

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    appointment_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Scheduled")

    # Foreign Keys
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)

    # Relationships
    customer = db.relationship("Customer", back_populates="appointments")
    staff = db.relationship("Staff", back_populates="appointments")
    appointmentservices = db.relationship("AppointmentService", back_populates="appointment")
