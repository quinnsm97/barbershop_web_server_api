from init import db

class Service(db.Model):
     __tablename__ = "services"
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(50), unique=True, nullable=False)
     price = db.Column(db.Float, nullable=False)
     duration_minutes = db.Column(db.Integer, default=30)