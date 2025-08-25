from flask import Blueprint, jsonify, request
from init import db
from models.service import Service
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from schemas.schemas import service_schemas, service_schema

service_bp = Blueprint("service", __name__, url_prefix="/services")

# Routes
# GET /
@service_bp.route("/")
def get_services():
    # Define the GET statement
    # SELECT * FROM services;
    stmt = db.select(Service)
    services_list = db.session.scalars(stmt) # Python object
    data = service_schemas.dump(services_list) # JavaScript JSON object

    if data:
        return jsonify(data)
    else:
        return {"message": "No service records found."}, 404
    
# GET /id
@service_bp.route("/<int:id>")
def get_a_service(id):
    # Define a statement
    stmt = db.select(Service).where(Service.id == id)
    # Execute
    service = db.session.scalar(stmt)

    if service:
        # Serialise
        data = service_schema.dump(service)
        # Return data
        return jsonify(data)
    else:
        return {"message": f"Service with id {id} does not exist"}, 404

# POST /
@service_bp.route("/", methods=["POST"])
def create_a_service():
    try:
        # GET info from REQUEST body
        body_data = request.get_json()
        # Create a Service object from Service class with body response data
        new_service = Service(
            name = body_data.get("name"),
            price = body_data.get("price"),
            duration_minutes = body_data.get("duration_minutes"),
            description = body_data.get("description")
        ) 
        # Add the new service data to the session
        db.session.add(new_service)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(service_schema.dump(new_service))
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            constraint = err.orig.diag.constraint_name

            # Map constraint names to user-friendly messages
            constraint_map = {
                "services_name_key": "name",
                "services_price_key": "price"
            }

            column = constraint_map.get(constraint, "field")
            return {"message": f"{column} must be unique"}, 400
        
        else: 
            return {"message": "Unexpected error occured"}, 400

# DELETE /id
@service_bp.route("/<int:id>", methods=["DELETE"])
def delete_service(id):
    # Find service with id
    stmt = db.select(Service).where(Service.id == id)
    service = db.session.scalar(stmt)
    # Validation (if exists)
    if service:
        db.session.delete(service)
        db.session.commit()

        return {"message": f"Service with id '{id}' has been removed successfully"}, 200
    else:
        return {"message": f"Service with id '{id}' does not exist"}, 404
    
# PUT/PATCH /id
@service_bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update_service(id):
    # Retrieve via id
    stmt = db.select(Service).where(Service.id == id)
    service = db.session.scalar(stmt)
    
    if service:
        # Retrieve data to be updated
        body_data = request.get_json()
        # Make changes
        service.name = body_data.get("name") or service.name
        service.price = body_data.get("price") or service.price
        service.duration_minutes = body_data.get("duration_minutes") or service.duration_minutes
        service.description = body_data.get("description") or service.description
        # Commit
        db.session.commit()
        # Return
        return jsonify(service_schema.dump(service))
    else:
        # Return with error message
        return {"message": f"Service with id {id} does not exist"}, 404

