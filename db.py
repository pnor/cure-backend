"""
File name: db.py
Author: Phillip O'Reggio
Date Created: 4/15/2019
Date Last Modified: 4/28/2019
Python Version: 3.0

Store SQLAlchemy database models for apps, tests, and results. Created for the 2019 Spring Semester
Hack Challenge.
"""
__author__ = "Phillip O'Reggio"

from flask_sqlalchemy import SQLAlchemy
import enum
import requests

db = SQLAlchemy()

class MethodType(enum.Enum):
    """
    All possible method types
    """
    get = 'GET'
    post = 'POST'
    put = 'PUT'
    patch = 'PATCH'
    delete = 'DELETE'

    def serialize(self):
        """ Return: the string representation """
        return self.value

    def get_requests_method(self):
        """ Return the requests method corresponding to this enum """
        if self is self.get:
            return requests.get
        elif self is self.post:
            return requests.post
        elif self is self.put:
            return requests.put
        elif self is self.patch:
            return requests.patch
        elif self is self.delete:
            return requests.delete
        else: 
            print('Input type not handled/Invalid')
            return None

class Base(db.Model):
    """
    Base model that all other models extend. Has columns all models have such as createdAt and
    updatedAt.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.Integer, nullable=False)
    updatedAt = db.Column(db.Integer, nullable=False)

class App(Base):
    """
    SQLAlchemy Representation for an App. Apps have tests to run
    """
    __tablename__ = 'app' 
    name = db.Column(db.Text, nullable=False)
    icon = db.Column(db.Text, nullable=False)
    tests = db.relationship('Test', cascade='delete')

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.icon = kwargs['icon']
        self.createdAt = kwargs['createdAt']
        self.updatedAt = kwargs['updatedAt']

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'tests': [test.serialize() for test in self.tests],
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

class Test(Base):
    """
    SQLAlchemy Representation for tests of an App. Each app has tests which store successes and failures
    """
    __tablename__ = 'test' 
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    method = db.Column(db.Enum(MethodType), nullable=False)
    parameters = db.Column(db.Text, nullable=True) # Dict as String
    app_id = db.Column(db.Integer, db.ForeignKey('app.id'), nullable=False)
    results = db.relationship('Result', cascade='delete')

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.url = kwargs['url']
        self.method = kwargs['method']
        self.parameters = kwargs['parameters']
        self.app_id = kwargs['app_id']
        self.createdAt = kwargs['createdAt']
        self.updatedAt = kwargs['updatedAt']

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'method': self.method.serialize(),
            'parameters': self.parameters,
            'results': [result.serialize() for result in self.results],
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt 
        }

class Result(Base):
    """
    SQLAlchemy Representation for successes and failures of tests.
    """
    __tablename__ = 'result' 
    success = db.Column(db.Boolean, nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)

    def __init__(self, **kwargs):
        self.success = kwargs['success']
        self.test_id = kwargs['test_id']
        self.createdAt = kwargs['createdAt']
        self.updatedAt = kwargs['updatedAt']

    def serialize(self):
        return {
            'id': self.id,
            'success': self.success,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }
