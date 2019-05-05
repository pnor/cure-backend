# Cure (backend)
Your server's status is always a tap away.
[TODO add app icon]

#### Cure front-end
[link coming soon!]

This repo contains the code for the backend that provides information for Cure. Cure was created to allow members of Cornell Appdev to be able to better monitor the status of the server's their apps rely on to function. With timestamped success and failure times, and the ability to graph the results of multiple tests over the course of a day, the team will be able document and react to unexptected server disturbances 24-7. 
 
This backend was built using [Flask](https://flask-sqlalchemy.palletsprojects.com/en/2.x/ ) and [SQLAlchemy](https://www.sqlalchemy.org), and deployed on Google Cloud Servers.

### Run Locally
Activate a python virtual enviroment and install necessary requirements with `pip install -r requirements.txt`. Then run with:
```python app.py```
