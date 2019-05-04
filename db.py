"""
File name: db.py
Author: Phillip O'Reggio
Python Version: 3.0

Store SQLAlchemy database models for apps, tests, and results. Created for the 2019 Spring Semester
Hack Challenge.
"""
__author__ = "Phillip O'Reggio"

import datetime
import enum
import hashlib
import os
import time

import bcrypt
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

import constants

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

class User(Base):
    """
    SQLAlchemy Represention of a User. Stores Username, password, and tokens
    """
    __tablename__ = 'user'
    # User Info
    email = db.Column(db.String, nullable=False)
    password_digest = db.Column(db.String, nullable=False)
    # Tokens
    session_token = db.Column(db.String, nullable=False, unique=True)
    expiration_token = db.Column(db.DateTime, nullable=False, unique=True)
    update_token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, **kwargs):
        unix_time = int(time.time())
        self.email = kwargs['email']
        self.password_digest= bcrypt.hashpw(kwargs['password'].encode('utf8'), bcrypt.gensalt(rounds=13))
        self.createdAt = kwargs['createdAt']
        self.updatedAt= kwargs['updatedAt']
        self.renew_session()
        self.createdAt = unix_time
        self.updatedAt = unix_time 

    def serialize(self):
        return {
            'email': str(self.email),
            'password_digest': str(self.password_digest),
            'session_token': str(self.session_token),
            'expiration_token': str(self.expiration_token),
            'update_token': str(self.update_token)
        }

    def renew_session(self):
        """
        Generates new session, expiration, and update tokens for a user
        """
        self.session_token = self._urlsafe_base_64()
        self.expiration_token = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()
        self.updatedAt = int(time.time())

    def _urlsafe_base_64(self):
        """
        Generates session/update tokens
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def verify_password(self, password):
        """
        Verifies a user's password
        """
        return bcrypt.checkpw(password.encode('utf8'), self.password_digest) 

    def verify_session_token(self, session_token):
        """
        Verifies a user's session token
        """
        return session_token == self.session_token and datetime.datetime.now() < self.expiration_token 

    def verify_update_token(self, update_token):
        """
        Verifies a user's update token
        """
        return update_token == self.update_token

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
        checksPassed, totalChecks = self.get_latest_results()
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'totalChecks': totalChecks,
            'numChecksPassed': checksPassed,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

    def get_latest_results(self):
        """
        Returns a tuple of the number of tests passed, and the total number of tests
        """
        tests = self.tests 

        results = []
        for test in tests:
            # Get latest test belonging to app
            subqry = db.session.query(func.max(Result.createdAt)).filter(Result.test_id == test.id)
            result = db.session.query(Result).filter(Result.test_id == test.id, Result.createdAt == subqry)
            results.append(result.first())

        # Handle tests that have no results (treat as "success")
        successes = 0
        total_tests = len(tests) if len(tests) != 0 else 1
        for result in results:
            if result is None:
                successes += 1
            else:
                successes += result.success

        return successes, total_tests 

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
            'results': [result.serialize() for result in self.results[-constants.MAX_RESULTS:]],
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
