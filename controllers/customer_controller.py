from flask import Blueprint, jsonify, request
from init import db
from models.customer import Customer, customer_schemas, customer_schema

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

# Routes
# GET /
@customer_bp.route("/")
def get_students():
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
# PUT/PATCH /id
# DELETE /id