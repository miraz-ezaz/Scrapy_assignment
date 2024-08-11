import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from urllib.parse import urlparse
from .config import DATABASE_URL
from .models import Base, Listing

def init_db():
    # Parse the database URL to get the database name
    parsed_url = urlparse(DATABASE_URL)
    db_name = parsed_url.path[1:]  # Remove the leading '/'

    # Create the database engine
    engine = create_engine(DATABASE_URL)

    # Check if the database exists, if not, create it
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database '{db_name}' created.")
    else:
        print(f"Database '{db_name}' already exists.")

    # Create tables if they do not exist
    Base.metadata.create_all(engine)

    # Create a session factory
    Session = sessionmaker(bind=engine)
    return Session

def add_listing(session, title, rating, location, latitude, longitude, room_type, price, images):
    new_listing = Listing(
        title=title,
        rating=rating,
        location=location,
        latitude=latitude,
        longitude=longitude,
        room_type=room_type,
        price=price,
        images=images
    )
    session.add(new_listing)
    session.commit()
