from flask import Blueprint
from init import db
from models.appointment_service import AppointmentService
from models.customer import Customer
from models.service import Service
from models.staff import Staff
from models.appointment import Appointment

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

    services = [
        Service(
            name="Fade",
            price=25.0,
            duration_minutes=30,
            description="Classic fade haircut"
        ),
        Service(
            name="Scissor Cut",
            price=25.0,
            duration_minutes=40,
            description="Precision scissor cut for a clean look"
        ),
        Service(
            name="Shampoo",
            price=15.0,
            duration_minutes=20,
            description="Hair wash and scalp massage"
        ),
        Service(
            name="Colour",
            price=50.0,
            duration_minutes=60,
            description="Full colour or highlights"
        ),
        Service(
            name="Kids Cut",
            price=20.0,
            duration_minutes=25,
            description="Haircut for children aged 3-12"
        ),
        Service(
            name="Buzz Cut",
            price=20.0,
            duration_minutes=15,
            description="Quick and simple buzz cut"
        )
    ]

    db.session.add_all(services)

    from datetime import datetime, timedelta

    appointments = [
        Appointment(
            appointment_datetime=datetime(2025, 8, 22, 10, 0),
            status="Scheduled",
            customer_id=1,
            staff_id=1
        ),
        Appointment(
            appointment_datetime=datetime(2025, 8, 22, 11, 0),
            status="Completed",
            customer_id=2,
            staff_id=2
        ),
        Appointment(
            appointment_datetime=datetime(2025, 8, 23, 9, 30),
            status="Cancelled",
            customer_id=1,
            staff_id=3
        ),
    ]
    db.session.add_all(appointments)

    appointment_services = [
        # Appointment 1: Fade + Shampoo
        AppointmentService(appointment_id=1, service_id=1),
        AppointmentService(appoinment_id=1, service_id=3),

        # Appointment 2: Scissor Cut
        AppointmentService(appoinment_id=2, service_id=2),

        # Appointment 3: Kids Cut
        AppointmentService(appoinment_id=3, service_id=5),
    ]

    db.session.add_all(appointment_services)
    # Commit
    db.session.commit()

    print("Tables seeded.")