#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import urllib.parse
import os
from models.place import Place, place_amenity
from models.city import City
from models.user import User
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review
from models.state import State

class DBStorage:
    """Creation of a SQL database for hbnb models"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization of the DB """
        usr = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        st = os.getenv('HBNB_MYSQL_HOST')
        dbn = os.getenv('HBNB_MYSQL_DB')
        vnt = os.getenv('HBNB_ENV')
        Db_URL = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            usr, pwd, st, dbn
        )
        self.__engine = create_engine(
            Db_URL,
            pool_pre_ping=True
        )
        if vnt == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, clas=None):
        """the return is a dict of the stored models"""
        bjts = dict()
        all_classes = (User, State, City, Amenity, Place, Review)
        if clas is None:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    objk = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    bjts[objk] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                objk = '{}.{}'.format(obj.__class__.__name__, obj.id)
                bjts[obk] = obj
        return bjts

    def delete(self, elm=None):
        """The funct remore an object from the given DB"""
        if elm is not None:
            self.__session.query(type(obj)).filter(
                type(elm).id == elm.id).delete(
                synchronize_session=False
            )

    def new(self, elm):
        """The funct adds new object to DB"""
        if elm is not None:
            try:
                self.__session.add(elm)
                self.__session.flush()
                self.__session.refresh(elm)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """Display the changes of the DB"""
        self.__session.commit()

    def reload(self):
        """The function loads the given DB"""
        Base.metadata.create_all(self.__engine)
        SessionFactory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(SessionFactory)()

    def close(self):
        """The function to close."""
        self.__session.close()
