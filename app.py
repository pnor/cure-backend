"""
File name: db.py
Author: Phillip O'Reggio
Python Version: 3.0

Specifies all methods and their endpoints. Created for the 2019 Spring Semester
Hack Challenge.
"""
__author__ = "Phillip O'Reggio"

import constants
import json
import threading
import time
import datetime
from flask import Flask, request
from db import db, App, Test, Result, MethodType

app = Flask(__name__)
db_filename = 'database.db'

# Configure flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return 'Hello world!'

#--- Database Maintenance
def initialize_empty():
    """ 
    Initializes the database with 4 apps, each with a root test

    Return: List of the 4 App objects and a List of 4 Test objects
    """
    curTime = int(time.time())
    eatery = App(
        name = 'Eatery',
        icon = 'https://raw.githubusercontent.com/cuappdev/assets/master/app-icons/Eatery-83.5x83.5%402x.png',
        createdAt = curTime,
        updatedAt = curTime
    ) 
    db.session.add(eatery)
    eatery_test1 = Test(
        name = 'Campus Eateries Test',
        url = 'https://eatery-backend.cornellappdev.com/',
        method = MethodType('GET'),
        parameters = 'query{eateries{name}}',
        is_graphql = True,
        results = [],
        app_id = 1,
        createdAt = curTime,
        updatedAt = curTime
    )
    
    eatery_test2 = Test(
        name = 'CTown Eateries Test',
        url = 'https://eatery-backend.cornellappdev.com/',
        method = MethodType('GET'),
        parameters = 'query{collegetownEateries{name}}',
        is_graphql = True,
        results = [],
        app_id = 1,
        createdAt = curTime,
        updatedAt = curTime
    )
    db.session.add(eatery_test1)
    db.session.add(eatery_test2)

    curTime = int(time.time())
    uplift = App(
        name = 'Uplift',
        icon = 'https://raw.githubusercontent.com/cuappdev/assets/master/app-icons/Uplift-83.5x83.5%402x.png',
        createdAt = curTime,
        updatedAt = curTime
    )
    db.session.add(uplift)
    uplift_test1=Test(
        name = 'Campus Gyms Test',
        url = 'http://uplift-backend.cornellappdev.com/',
        method = MethodType('GET'),
        parameters = 'query{gyms{description}}',
        is_graphql = True,
        results = [],
        app_id = 2,
        createdAt = curTime,
        updatedAt = curTime
    )
    uplift_test2=Test(
        name = 'Gym Classes Test',
        url = 'http://uplift-backend.cornellappdev.com/',
        method = MethodType('GET'),
        parameters = 'query{classes{id}}',
        is_graphql = True,
        results = [],
        app_id = 2,
        createdAt = curTime,
        updatedAt = curTime
    )
    db.session.add(uplift_test1)
    db.session.add(uplift_test2)

    curTime = int(time.time())
    transit= App(
        name = 'Transit',
        icon = 'https://raw.githubusercontent.com/cuappdev/assets/master/app-icons/Transit-83.5x83.5%402x.png',
        createdAt = curTime,
        updatedAt = curTime
    )
    db.session.add(transit)
    transit_test= Test(
        name = 'Node Microservice Test',
        url = 'http://transit-backend.cornellappdev.com/api/v1/',
        method = MethodType('GET'),
        parameters = '',
        results = [],
        app_id = 3,
        createdAt = curTime,
        updatedAt = curTime
    )
    db.session.add(transit_test)

    curTime = int(time.time())
    pollo = App(
        name = 'Pollo',
        icon = 'https://raw.githubusercontent.com/cuappdev/assets/master/app-icons/pollo-1024%401x.png',
        createdAt = curTime,
        updatedAt = curTime
    )
    db.session.add(pollo)
    pollo_test = Test(
        name = 'Root Test',
        url = 'http://transit-backend.cornellappdev.com/api/v1/',
        method = MethodType('GET'),
        parameters = '',
        results = [],
        app_id = 4,
        createdAt = curTime,
        updatedAt = curTime
    )
    db.session.add(pollo_test)
    
    db.session.commit()


# @app.route('/api/delete/everything/')
def delete_everything():
    """ Deletes all tables and the data it contains """
    db.reflect()
    db.drop_all() 
    return json.dumps({'success': True, 'data': 'All tables dropped'}), 200

# @app.route('/api/clear/everything')
def clear_data():
    """ Clears all data from all tables """
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
    return json.dumps({'success': True, 'data': 'All data cleared'}), 20

@app.route('/api/results/clear/', methods=['DELETE'])
def clear_results():
    """ Clears all results from tests """
    db.session.query(Result).delete()
    db.session.commit()
    return json.dumps({'success': True, 'data': 'Results cleared'}), 200

#--- App

# Get all Apps
@app.route('/api/apps/')
def get_all_apps():
    """ Return all apps"""
    apps = App.query.all()
    res = {'success': True, 'data': [app.serialize() for app in apps]}
    return json.dumps(res), 200

# Get app at
@app.route('/api/app/<int:app_id>/')
def get_app_at(app_id):
    """ Get app at position"""
    app = App.query.filter_by(id=app_id).first()
    if app is not None:
        return json.dumps({'success': True, 'data': app.serialize()}), 200

    return json.dumps({'success': False, 'data': 'App not found'}), 404

# Create an App
@app.route('/api/apps/', methods=['POST'])
def create_app():
    """ Creates and stores new App"""
    body = json.loads(request.data)
    unix_time = int(time.time())
    new_app = App(
        name = body['name'],
        icon = body['icon'],
        createdAt = unix_time,
        updatedAt = unix_time 
    )
    db.session.add(new_app)
    db.session.commit()
    return json.dumps({'success': True, 'data': new_app.serialize()}), 201

# Delete an App
@app.route('/api/app/<int:app_id>/', methods=['DELETE'])
def delete_app(app_id):
    """ Deletes app at position """
    deleted_app = App.query.filter_by(id=app_id).first()
    if deleted_app is not None:
        db.session.delete(deleted_app)
        db.session.commit()
        return json.dumps({'success': True, 'data': deleted_app.serialize()}), 200

    return json.dumps({'success': False, 'data': 'App not found'}), 404

#--- Test

# Get all Tests
@app.route('/api/tests/')
def get_all_tests():
    """ Gets all stored tests for all apps """
    tests = Test.query.all()
    res = {'success': True, 'data': [test.serialize() for test in tests]}
    return json.dumps(res), 200

# Get all Tests for an app
@app.route('/api/tests/<int:app_id>/')
def get_all_tests_for_app(app_id):
    """ Get all tests for an app at id """
    app = App.query.filter_by(id=app_id).first()
    if app is not None:
        all_tests = [test.serialize() for test in app.tests]
        return json.dumps({'success': True, 'data': all_tests}), 200
    
    return json.dumps({'success': False, 'data': 'App not found'}), 404

# Create a Test
@app.route('/api/test/<int:app_id>/', methods=['POST'])
def create_test(app_id):
    """ Create a test for app at id """
    app = App.query.filter_by(id=app_id).first()
    if app is not None:
        body = json.loads(request.data)
        unix_time = int(time.time())
        test = Test(
            app_id = app.id,
            name = body['name'] if body['name'] is not None else "",
            url = body['url'],
            method = MethodType(body['method']),
            parameters = body['parameters'],
            is_graphql = body.get('is_graphql', False),
            createdAt = unix_time,
            updatedAt = unix_time 
        ) 
        app.updatedAt = unix_time
        db.session.add(test)
        db.session.commit()
        return json.dumps({'success': True, 'data': test.serialize()}), 201

    return json.dumps({'success': False, 'data': 'App not found'}), 404

# Remove a Test
@app.route('/api/test/<int:test_id>/', methods=['DELETE'])
def delete_test(test_id):
    """ Delete a specific test for an app """
    test = Test.query.filter_by(id=test_id).first()
    if test is not None:
        unix_time = int(time.time())
        app = App.query.filter_by(id=test.app_id).first()
        app.updatedAt = unix_time
        db.session.delete(test)
        db.session.commit()
        return json.dumps({'success': True, 'data': test.serialize()}), 200

    return json.dumps({'success': False, 'data': 'Test not found'}), 404

#--- Results

# Get all Results for an App (Numeric, Now)
@app.route('/api/results-now/<int:app_id>/')
def get_test_results_now(app_id):
    """ 
    Get the number of latest passed and failed tests for an app. Calculates it when requested.
    """
    app = App.query.filter_by(id=app_id).first()
    if app is not None:
        tests = app.tests 
        successes = []
        for test in tests:
            successful, result_obj = run_test(test, graphql=test.is_graphql)
            successes.append(successful)
            db.session.add(result_obj) 
        # Update updatedAt
        app.updatedAt = int(time.time())

        db.session.commit()
        data = {
            'success': sum(successes),
            'total': len(tests) if len(tests) != 0 else 1 # Prevent this from being 0
        }
        return json.dumps({'success': True, 'data': data}), 200

    return json.dumps({'success': False, 'data': 'App not found'}), 404

# Get latest pass fails for an app 
@app.route('/api/results/<int:app_id>/')
def get_test_results(app_id):
    """ Gets the number of passed and failed tests for an app from last time tests were run """
    app = App.query.filter_by(id=app_id).first()
    if app is not None:
        successes, total = app.get_latest_results()
         
        data = {
            'success': successes,
            'total': total 
        }
        return json.dumps({'success': True, 'data': data}), 200

    return json.dumps({'success': False, 'data': 'App not fond'}), 404

# Get all historical results for a test
@app.route('/api/results/history/<int:test_id>/')
def get_historical_data(test_id):
    test = Test.query.filter_by(id=test_id).first()
    if test is not None:
        results = test.results[-constants.MAX_RESULTS:]
        res = [result.serialize() for result in results]
        return json.dumps({'success': False, 'data': res}), 200

    return json.dumps({'success': False, 'data': 'Test not found'}), 404

#--- Not networking

# Periodic run tests on everything
def test_apps():
    """
    Tests every test contained by each app and stores the results. Is called periodically
    """
    with app.app_context():
        # Run tests
        tests = Test.query.all()
        for test in tests:
            successful, result_obj = run_test(test, graphql=test.is_graphql)
            db.session.add(result_obj) 

        # Update apps
        apps = App.query.all()
        unix_time = int(time.time())
        for a in apps:
            a.updatedAt = unix_time
            
        db.session.commit()

def exec_every_n_seconds(n,f):
    """
    Executes a method every n seconds (using a single thread, accounting for time drift)
    https://stackoverflow.com/questions/8600161/executing-periodic-actions-in-python/20169930#20169930
    """
    first_called=datetime.datetime.now()
    f()
    num_calls=1
    drift= datetime.timedelta()
    time_period=datetime.timedelta(seconds=n)
    while 1:
        time.sleep(n-drift.microseconds/1000000.0)
        current_time = datetime.datetime.now()
        f()
        num_calls += 1
        difference = current_time - first_called
        drift = difference - time_period* num_calls


# Running Tests
def run_test(test, graphql=False, log_data=True):
    """
    Runs a test stored in the database.
    Return: Tuple. First element is a boolean that is True if passed with an "OK" error code,
     False otherwise. Second is the Result object to be stored in the database.
     If log_data is False, it will only return the boolean (no tuple)
    """
    # Here "valid" means its a 200 code
    is_valid_error_code = lambda code: code - 200 < 100 and code - 200 >= 0
    # Get info for test
    endpoint = test.url
    method = test.method
    try:
        if graphql: # Make graphql request
            parameters = test.parameters
            no_whitespace = parameters.replace(' ', '').replace('\n', '').replace('\t', '')
            endpoint = endpoint + '?query=' + no_whitespace
            parameters = '' 
        else: # normal request
            parameters = dict(test.parameters)
    except: # Error, likely from graphql/normal request mismatch
        # Treat as failure
        if log_data:
            unix_time = int(time.time())
            result = Result(
                test_id = test.id,
                success = False,
                createdAt = unix_time,
                updatedAt = unix_time
            )
            return False, result
        else:
            return False 

    # Make request
    request_type = method.get_requests_method()
    response = request_type(endpoint, data=parameters)

    # Get result and store in database
    result_bool = is_valid_error_code(response.status_code) 
    
    if log_data:
        unix_time = int(time.time())
        result = Result(
            test_id = test.id,
            success = result_bool,
            createdAt = unix_time,
            updatedAt = unix_time
        )
        return result_bool, result
    else:
        return result_bool

if __name__ == '__main__':
    # Initialize apps
    with app.app_context():
        if App.query.first() is None: # Is empty: initialize with 4 apps
            initialize_empty()

    # Setup Periodic Tests
    threading.Thread(target=exec_every_n_seconds, args=(constants.TESTING_TIME_PERIOD, test_apps)).start()

    app.run(host='0.0.0.0', port=5000, debug=False)
elif __name__ == 'app': 
    pass
