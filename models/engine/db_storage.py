#!/usr/bin/python3
"""This module defines a class to manage db storage for Foodify"""
from contextlib import contextmanager
from typing import Dict, Any, Optional, List
from models.review import Review
from models.restaurant import Restaurant
from models.order import Order
from models.order_item import OrderItem
from models.menu_item import MenuItem
from models.client import Client
from models.base_model import Base, BaseModel
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from os import getenv
from dotenv import load_dotenv
load_dotenv()


classes = [Client, Restaurant, MenuItem, Review, Order, OrderItem]


class DBStorage:
    """Database Storage Class"""

    __engine = None
    __session = None

    def __init__(self) -> None:
        """Initialize database connection with better settings"""
        user = getenv("FOOD_MYSQL_USER")
        pwd = getenv("FOOD_MYSQL_PWD")
        host = getenv("FOOD_MYSQL_HOST")
        db = getenv("FOOD_MYSQL_DB")

        if not all([user, pwd, host, db]):
            raise ValueError("Missing required database credentials")

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
            pool_pre_ping=True,  # Check connection before using
            pool_recycle=300,  # Recycle connections every 5 minutes
            pool_size=5,  # Smaller pool size
            max_overflow=10,  # Allow more temp connections if needed
            pool_timeout=30,  # Connection timeout
            connect_args={"connect_timeout": 60, "read_timeout": 30},
        )
        self.__session = None

    def reload(self) -> None:
        """Create tables and session with proper error handling"""
        try:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False, autoflush=True
            )
            Session = scoped_session(session_factory)
            self.__session = Session
        except Exception as e:
            print(f"Error reloading database: {e}")
            if self.__session:
                self.__session.remove()
            raise

    def new(self, obj: BaseModel) -> None:
        """Add object to current database session"""
        if obj:
            self.__session.add(obj)

    def save(self) -> None:
        """Commit changes to database"""
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            print(f"Error saving changes: {e}")  # Added error logging
            raise e

    def delete(self, obj: Optional[BaseModel] = None) -> None:
        """Delete object from current database session"""
        if obj:
            try:
                self.__session.delete(obj)
                self.__session.flush()  # Added flush() call
            except Exception as e:
                self.__session.rollback()
                print(f"Error deleting object: {e}")  # Added error logging

    def get(self, cls: Any, id: str) -> Optional[BaseModel]:
        """Retrieve object by class and id"""
        if cls and id:
            return self.__session.query(cls).filter(cls.id == id).first()
        return None

    def all(self, cls=None) -> Dict[str, BaseModel]:
        """Query objects"""
        try:
            if cls:
                objects = self.__session.query(cls).all()
            else:
                objects = []
                for c in classes:
                    objects.extend(self.__session.query(c).all())

            return {
                f"{obj.__class__.__name__}.{obj.id}": obj for obj in objects
            }

        except Exception as e:
            self.__session.rollback()
            raise e

    def search(
        self,
        cls: Any,
        filters: Dict[str, Any],
        nested_filters: Dict[str, Dict] = None,
    ) -> List[BaseModel]:
        """
        Enhanced search method with nested relationship filtering

        Example:
        filters = {"name": "Pizza Hut"}
        nested_filters = {"menu_items": {"name": "juice"}}
        """
        query = self.__session.query(cls)

        # Apply main filters
        for key, value in filters.items():
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key).ilike(f"%{value}%"))

        # Apply nested filters
        if nested_filters:
            for relation, rel_filters in nested_filters.items():
                if hasattr(cls, relation):
                    for key, value in rel_filters.items():
                        query = query.filter(
                            getattr(cls, relation).any(**{key: value})
                        )

        return query.all()

    def close(self) -> None:
        """Close session safely"""
        if self.__session:
            try:
                self.__session.remove()  # Safe to call on scoped_session
            except Exception as e:
                print(f"Error closing session: {e}")
                pass

    def count(self, cls: Optional[Any] = None) -> int:
        """Count number of objects in storage"""
        if cls:
            return self.__session.query(cls).count()
        return 0

    def rollback(self) -> None:
        """Rollback current database session"""
        try:
            if self.__session:
                self.__session.rollback()
        except Exception as e:
            print(f"Error during rollback: {e}")

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations"""
        session = self.refresh_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            if session:
                session.rollback()
            print(f"Session error: {e}")
            raise
        finally:
            if session:
                session.remove()  # Now safe to call remove() on scoped_session

    def refresh_session(self):
        """Create a fresh session"""
        try:
            if self.__session:
                self.__session.close()  # Use close() instead of remove() for regular sessions

            # Create session factory
            session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False, autoflush=True
            )
            # Create scoped session
            Session = scoped_session(session_factory)
            self.__session = Session
            return self.__session
        except Exception as e:
            print(f"Error refreshing session: {e}")
            raise
