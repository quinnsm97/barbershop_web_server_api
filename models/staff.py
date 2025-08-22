from init import db


class Staff(db.Model):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    specialty = db.Column(db.String(100))

    # Relationship to appointments
    appointments = db.relationship("Appointment", back_populates="staff", cascade="all, delete")

