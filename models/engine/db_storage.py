#!/usr/bin/python3
"""This module defines a class to manage db storage for Foodify"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.clients import Client


class DBStorage():
    """ DBStorage class """
    engine = None  # Holds the SQLAlchemy engine (connection manager)
    session = None  # Holds the database session (workspace)

    def __init__(self):
        """Initializes the DBStorage engine"""

        USER = getenv('Foodify_MYSQL_USER')
        PWD = getenv('Foodify_MYSQL_PWD')
        HOST = getenv('Foodify_MYSQL_HOST')
        DB = getenv('Foodify_MYSQL_DB')
        ENV = getenv('Foodify_ENV')

        # Create the connection string using environment variables
        conn_str = f"mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}"

        # Create the SQLAlchemy engine (connection manager)
        self.engine = create_engine(conn_str, pool_pre_ping=True)

        if ENV == 'test':
            # Drop all tables for testing
            Base.metadata.drop_all(self.engine)
            print("All tables dropped because Foodify_ENV is set to 'test'.")

    def all(self, cls=None):
        """Queries the database for all objects of a given class"""
        objects = {}
        if cls is None:
            # Query all types of objects
            for model_class in [Client]:
                for obj in self.session.query(model_class).all():
                    key = f"{model_class.__name__}.{obj.id}"
                    objects[key] = obj
        else:
            # Query only objects of the specified class
            for obj in self.session.query(cls).all():
                key = f"{cls.__name__}.{obj.id}"
                objects[key] = obj
        return objects

    def new(self, obj):
        """Adds an object to the current database session"""
        self.session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session"""
        if obj is not None:
            self.session.delete(obj)

    def reload(self):
        """Creates all tables and a new session"""

        # Create all tables
        Base.metadata.create_all(self.engine)

        # Create a session factory
        session_factory = sessionmaker(bind=self.engine,
                                        expire_on_commit=False)

        # Create a thread-safe session using scoped_session
        self.session = scoped_session(session_factory)

    def close(self):
        """Call remove() method on the private session attribute"""
        self.session.remove()