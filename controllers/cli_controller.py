from flask import Blueprint
from init import db
from models.customer import Customer
from models.staff import Staff

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
    staff_members = [
        Staff(
            first_name="Jordan",
            last_name="Smith",
            role="Barber",
            specialty="Fades"
        ),
        Staff(
            first_name="Alicia",
            last_name="Brown",
            role="Barber",
            specialty="Scissor Cuts"
        ),
        Staff(
            first_name="Marcus",
            last_name="Johnson",
            role="Apprentice",
            specialty="Shampoo"
        ),
        Staff(
            first_name="Sophie",
            last_name="Lee",
            role="Receptionist",
            specialty="N/A"
        ),
        Staff(
            first_name="Daniel",
            last_name="White",
            role="Barber",
            specialty="Kids Cuts"
        ),
        Staff(
            first_name="Priya",
            last_name="Patel",
            role="Barber",
            specialty="Coloring"
        ),
        Staff(
            first_name="Tom",
            last_name="Wilson",
            role="Barber",
            specialty="Buzz Cuts"
        )
    ]
    db.session.add_all(customers)
    db.session.add_all(staff_members)
    # Commit
    db.session.commit()

    print("Tables seeded.")