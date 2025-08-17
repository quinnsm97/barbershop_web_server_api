from flask import Blueprint, jsonify
from init import db
from models.customer import Customer, customer_schemas

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
# POST /
# PUT/PATCH /id
# DELETE /id