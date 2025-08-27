from flask import Blueprint, jsonify, request
from init import db
from models.appointment import Appointment
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from schemas.schemas import appointment_schemas, appointment_schema

appointment_bp = Blueprint("appointment", __name__, url_prefix="/appointments")

ALLOWED_STATUS = ["Scheduled", "Completed", "Cancelled"]

# Routes
# GET /
@appointment_bp.route("/")
def get_appointments():
    """
    Retrieve all appointment records ordered by appointment datetime.

    Returns:
        Response: JSON array of appointment records or a 404 error message if none found.
    """
    # Define the GET statement
    # SELECT * FROM appointments;
    stmt = db.select(Appointment).order_by(Appointment.appointment_datetime)
    appointments_list = db.session.scalars(stmt) # Python object
    data = appointment_schemas.dump(appointments_list) # JavaScript JSON object

    if data:
        return jsonify(data)
    else:
        return {"message": "No appointment records found."}, 404
    
# GET /id
@appointment_bp.route("/<int:id>")
def get_a_appointment(id):
    """
    Retrieve a single appointment record by its ID.

    Args:
        id (int): The ID of the appointment to retrieve.

    Returns:
        Response: JSON object of the appointment record or a 404 error message if not found.
    """
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
    """
    Create a new appointment record with the provided data.

    Expects JSON body with keys: appointment_datetime, status, customer_id, staff_id.

    Returns:
        Response: JSON object of the created appointment record with status 201,
                  or error message with status 400 on validation or integrity errors.
    """
    try:
        # Get info from request body
        body_data = request.get_json()

        # Validate status
        status = body_data.get("status")
        if status not in ALLOWED_STATUS:
            return jsonify({"error": f"Invalid status. Allowed values: {ALLOWED_STATUS}"}), 400

        # Create a new Appointment object
        new_appointment = Appointment(
            appointment_datetime=body_data.get("appointment_datetime"),
            status=status,
            customer_id=body_data.get("customer_id"),
            staff_id=body_data.get("staff_id")
        )

        # Add the new appointment data to the session
        db.session.add(new_appointment)
        db.session.commit()

        # Return the new appointment
        return jsonify(appointment_schema.dump(new_appointment)), 201

    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 400

# DELETE /id
@appointment_bp.route("/<int:id>", methods=["DELETE"])
def delete_appointment(id):
    """
    Delete an appointment record by its ID.

    Args:
        id (int): The ID of the appointment to delete.

    Returns:
        Response: Success message with status 200 if deleted,
                  or error message with status 404 if appointment not found.
    """
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
    """
    Update an existing appointment record by its ID with provided data.

    Args:
        id (int): The ID of the appointment to update.

    Expects JSON body with any of the keys: appointment_datetime, status, customer_id, staff_id.

    Returns:
        Response: JSON object of the updated appointment record,
                  or error message with status 404 if appointment not found,
                  or error message with status 400 if status is invalid.
    """
    # Retrieve via id
    stmt = db.select(Appointment).where(Appointment.id == id)
    appointment = db.session.scalar(stmt)
    
    if appointment:
        # Retrieve data to be updated
        body_data = request.get_json()
        # Validate status if being updated
        if "status" in body_data:
            if body_data["status"] not in ALLOWED_STATUS:
                return jsonify({"error": f"Invalid status. Allowed values: {ALLOWED_STATUS}"}), 400
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

