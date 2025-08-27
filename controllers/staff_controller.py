from flask import Blueprint, jsonify, request
from init import db
from models.staff import Staff
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from schemas.schemas import staff_schema, staff_schemas

staff_bp = Blueprint("staff", __name__, url_prefix="/staff")

# Routes
# GET /
@staff_bp.route("/")
def get_staff():
    """
    Retrieve a list of staff members, optionally filtered by specialty.

    Query Parameters:
        specialty (str): Optional specialty to filter staff by.

    Returns:
        JSON response containing a list of staff members if found,
        otherwise a 404 error message.
    """
    specialty = request.args.get("specialty")
    if specialty:
        stmt = db.select(Staff).where(Staff.specialty.ilike(specialty))
    else:
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
@staff_bp.route("/<int:id>")
def get_a_staff(id):
    """
    Retrieve a single staff member by their ID.

    Args:
        id (int): The ID of the staff member to retrieve.

    Returns:
        JSON response containing the staff member data if found,
        otherwise a 404 error message.
    """
    # Define a statement
    stmt = db.select(Staff).where(Staff.id == id)
    # Execute
    staff = db.session.scalar(stmt)

    if staff:
        # Serialise
        data = staff_schema.dump(staff)
        # Return data
        return jsonify(data)
    else:
        return {"message": f"Staff with id {id} does not exist"}, 404

# POST /
@staff_bp.route("/", methods=["POST"])
def create_a_staff():
    """
    Create a new staff member with the provided data.

    Expects JSON in the request body with keys:
        first_name (str), last_name (str), role (str), specialty (str).

    Returns:
        JSON response containing the created staff member data if successful,
        or an error message with status 400 if validation fails.
    """
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
@staff_bp.route("/<int:id>", methods=["DELETE"])
def delete_staff(id):
    """
    Delete a staff member by their ID.

    Args:
        id (int): The ID of the staff member to delete.

    Returns:
        A success message with status 200 if deletion is successful,
        or an error message with status 404 if the staff member does not exist.
    """
    # Find staff with id
    stmt = db.select(Staff).where(Staff.id == id)
    staff = db.session.scalar(stmt)
    # Validation (if exists)
    if staff:
        db.session.delete(staff)
        db.session.commit()

        return {"message": f"Staff with id '{id}' has been removed successfully"}, 200
    else:
        return {"message": f"Staff with id '{id}' does not exist"}, 404
    
# PUT/PATCH /id
@staff_bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update_staff(id):
    """
    Update an existing staff member's information by their ID.

    Args:
        id (int): The ID of the staff member to update.

    Expects JSON in the request body with any of the following keys:
        first_name (str), last_name (str), role (str), specialty (str).

    Returns:
        JSON response containing the updated staff member data if successful,
        or an error message with status 404 if the staff member does not exist.
    """
    # Retrieve via id
    stmt = db.select(Staff).where(Staff.id == id)
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
        return {"message": f"Staff with id {id} does not exist"}, 404

