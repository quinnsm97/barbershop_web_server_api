from flask import Blueprint, jsonify, request
from init import db
from models.staff import Staff, staff_schemas, staff_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

staff_bp = Blueprint("staff", __name__, url_prefix="/staff")

# Routes
# GET /
@staff_bp.route("/")
def get_staff():
    # Define the GET statement
    # SELECT * FROM staffs;
    stmt = db.select(Staff)
    staff_list = db.session.scalars(stmt) # Python object
    data = staff_schemas.dump(staff_list) # JavaScript JSON object

    if data:
        return jsonify(data)
    else:
        return {"message": "No staff records found."}, 404
    
# GET /id
@staff_bp.route("/<int:staff_id>")
def get_a_staff(staff_id):
    # Define a statement
    stmt = db.select(Staff).where(Staff.staff_id == staff_id)
    # Execute
    staff = db.session.scalar(stmt)

    if staff:
        # Serialise
        data = staff_schema.dump(staff)
        # Return data
        return jsonify(data)
    else:
        return {"message": f"Staff with id {staff_id} does not exist"}, 404

# POST /
@staff_bp.route("/", methods=["POST"])
def create_a_staff():
    try:
        # GET info from REQUEST body
        body_data = request.get_json()
        # Create a Staff object from Staff class with body response data
        new_staff = Staff(
            first_name = body_data.get("first_name"),
            last_name = body_data.get("last_name"),
            role = body_data.get("role"),
            specialty = body_data.get("specialty")
        )
        # Add the new staff data to the session
        db.session.add(new_staff)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(staff_schema.dump(new_staff))
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            constraint = err.orig.diag.constraint_name

            # Map constraint names to user-friendly messages
            constraint_map = {
                "staff_role_key": "role",
                "staff_specialty_key": "specialty"
            }

            column = constraint_map.get(constraint, "field")
            return {"message": f"{column} must be unique"}, 400
        
        else: 
            return {"message": "Unexpected error occured"}, 400

# DELETE /id
@staff_bp.route("/<int:staff_id>", methods=["DELETE"])
def delete_staff(staff_id):
    # Find staff with id
    stmt = db.select(Staff).where(Staff.staff_id == staff_id)
    staff = db.session.scalar(stmt)
    # Validation (if exists)
    if staff:
        db.session.delete(staff)
        db.session.commit()

        return {"message": f"Staff with id '{staff_id}' has been removed successfully"}, 200
    else:
        return {"message": f"Staff with id '{staff_id}' does not exist"}, 404
    
# PUT/PATCH /id
@staff_bp.route("/<int:staff_id>", methods=["PUT", "PATCH"])
def update_staff(staff_id):
    # Retrieve via id
    stmt = db.select(Staff).where(Staff.staff_id == staff_id)
    staff = db.session.scalar(stmt)
    
    if staff:
        # Retrieve data to be updated
        body_data = request.get_json()
        # Make changes
        staff.first_name = body_data.get("first_name") or staff.first_name
        staff.last_name = body_data.get("last_name") or staff.last_name
        staff.role = body_data.get("role") or staff.role
        staff.specialty = body_data.get("specialty") or staff.specialty
        # Commit
        db.session.commit()
        # Return
        return jsonify(staff_schema.dump(staff))
    else:
        # Return with error message
        return {"message": f"Staff with id {staff_id} does not exist"}, 404

