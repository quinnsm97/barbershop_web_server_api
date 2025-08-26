from flask import Blueprint, jsonify, request
from init import db
from models.appointment import Appointment
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from schemas.schemas import appointment_schemas, appointment_schema

appointment_bp = Blueprint("appointment", __name__, url_prefix="/appointments")

# Routes
# GET /
@appointment_bp.route("/")
def get_appointments():
    # Define the GET statement
    # SELECT * FROM appointments;
    stmt = db.select(Appointment)
    appointments_list = db.session.scalars(stmt) # Python object
    data = appointment_schemas.dump(appointments_list) # JavaScript JSON object

    if data:
        return jsonify(data)
    else:
        return {"message": "No appointment records found."}, 404
    
# GET /id
@appointment_bp.route("/<int:id>")
def get_a_appointment(id):
    # Define a statement
    stmt = db.select(Appointment).where(Appointment.id == id)
    # Execute
    appointment = db.session.scalar(stmt)

    if appointment:
        # Serialise
        data = appointment_schema.dump(appointment)
        # Return data
        return jsonify(data)
    else:
        return {"message": f"Appointment with id {id} does not exist"}, 404

# POST /
@appointment_bp.route("/", methods=["POST"])
def create_a_appointment():
    try:
        # GET info from REQUEST body
        body_data = request.get_json()
        # Create a Appointment object from Appointment class with body response data
        new_appointment = Appointment(
            appointment_datetime = body_data.get("appointment_datetime"),
            status = body_data.get("status"),
            customer_id = body_data.get("customer_id"),
            staff_id = body_data.get("staff_id")
        )
        # Add the new appointment data to the session
        db.session.add(new_appointment)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(appointment_schema.dump(new_appointment))
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return{"message": err.orig.diag.message_detail}, 400

# DELETE /id
@appointment_bp.route("/<int:id>", methods=["DELETE"])
def delete_appointment(id):
    # Find appointment with id
    stmt = db.select(Appointment).where(Appointment.id == id)
    appointment = db.session.scalar(stmt)
    # Validation (if exists)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()

        return {"message": f"Appointment with id '{id}' has been removed successfully"}, 200
    else:
        return {"message": f"Appointment with id '{id}' does not exist"}, 404
    
# PUT/PATCH /id
@appointment_bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update_appointment(id):
    # Retrieve via id
    stmt = db.select(Appointment).where(Appointment.id == id)
    appointment = db.session.scalar(stmt)
    
    if appointment:
        # Retrieve data to be updated
        body_data = request.get_json()
        # Make changes
        appointment.appointment_datetime = body_data.get("appointment_datetime") or appointment.appointment_datetime
        appointment.status = body_data.get("status") or appointment.status
        appointment.customer_id = body_data.get("customer_id") or appointment.customer_id
        appointment.staff_id = body_data.get("staff_id") or appointment.staff_id
        # Commit
        db.session.commit()
        # Return
        return jsonify(appointment_schema.dump(appointment))
    else:
        # Return with error message
        return {"message": f"Appointment with id {id} does not exist"}, 404

