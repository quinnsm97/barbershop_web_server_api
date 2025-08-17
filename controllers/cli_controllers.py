from flask import Blueprint
from init import db
from models.customer import Customer

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_table():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
    #Instance of the model
    customers = [
        Customer(
            first_name="Alice",
            last_name="Wonderland",
            email="alice@gmail.com",
            phone="0400000000"
        ), Customer(
            first_name="Bob",
            last_name="Builder",
            email="bob@gmail.com",
            phone="0400000001"
        )
    ]
    # Add to session
    db.session.add_all(customers)
    # Commit
    db.session.commit()

    print("Tables seeded.")