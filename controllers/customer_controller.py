from flask import Blueprint, jsonify
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
# PUT/PATCH /id
# DELETE /id