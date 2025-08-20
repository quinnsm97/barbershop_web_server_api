from flask import Blueprint, jsonify, request
from init import db
from models.customer import Customer, customer_schemas, customer_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

# Routes
# GET /
@customer_bp.route("/")
def get_customers():
    # Define the GET statement
    # SELECT * FROM customers;
    stmt = db.select(Customer)
    customers_list = db.session.scalars(stmt) # Python object
    data = customer_schemas.dump(customers_list) # JavaScript JSON object

    if data:
        return jsonify(data)
    else:
        return {"message": "No customer records found."}, 404
    
# GET /id
@customer_bp.route("/<int:customer_id>")
def get_a_customer(customer_id):
    # Define a statement
    stmt = db.select(Customer).where(Customer.customer_id == customer_id)
    # Execute
    customer = db.session.scalar(stmt)

    if customer:
        # Serialise
        data = customer_schema.dump(customer)
        # Return data
        return jsonify(data)
    else:
        return {"message": f"Customer with id {customer_id} does not exist"}, 404

# POST /
@customer_bp.route("/", methods=["POST"])
def create_a_customer():
    try:
        # GET info from REQUEST body
        body_data = request.get_json()
        # Create a Customer object from Customer class with body response data
        new_customer = Customer(
            first_name = body_data.get("first_name"),
            last_name = body_data.get("last_name"),
            email = body_data.get("email"),
            phone = body_data.get("phone")
        )
        # Add the new customer data to the session
        db.session.add(new_customer)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(customer_schema.dump(new_customer))
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            constraint = err.orig.diag.constraint_name

            # Map constraint names to user-friendly messages
            constraint_map = {
                "customers_email_key": "email",
                "customers_phone_key": "phone"
            }

            column = constraint_map.get(constraint, "field")
            return {"message": f"{column} must be unique"}, 400
        
        else: 
            return {"message": "Unexpected error occured"}, 400

# DELETE /id
@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    # Find customer with id
    stmt = db.select(Customer).where(Customer.customer_id == customer_id)
    customer = db.session.scalar(stmt)
    # Validation (if exists)
    if customer:
        db.session.delete(customer)
        db.session.commit()

        return {"message": f"Customer with id '{customer_id}' has been removed successfully"}, 200
    else:
        return {"message": f"Customer with id '{customer_id}' does not exist"}, 404
    
# PUT/PATCH /id
@customer_bp.route("/<int:customer_id>", methods=["PUT", "PATCH"])
def update_customer(customer_id):
    # Retrieve via id
    stmt = db.select(Customer).where(Customer.customer_id == customer_id)
    customer = db.session.scalar(stmt)
    
    if customer:
        # Retrieve data to be updated
        body_data = request.get_json()
        # Make changes
        customer.first_name = body_data.get("first_name") or customer.first_name
        customer.last_name = body_data.get("last_name") or customer.last_name
        customer.email = body_data.get("email") or customer.email
        customer.phone = body_data.get("phone") or customer.phone
        # Commit
        db.session.commit()
        # Return
        return jsonify(customer_schema.dump(customer))
    else:
        # Return with error message
        return {"message": f"Customer with id {customer_id} does not exist"}, 404

