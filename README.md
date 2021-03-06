# Cure (backend)
Your server's status is always a tap away.
<p align="center">
<img src=https://raw.githubusercontent.com/young-k/cure/master/Cure/Cure/Assets.xcassets/AppIcon.appiconset/aa180h.png>
</p>

<p align="center">
<img src=https://raw.githubusercontent.com/young-k/cure/master/Cure/Cure/Assets.xcassets/checkPassed.imageset/checkPassed.png> <img src=https://raw.githubusercontent.com/young-k/cure/master/Cure/Cure/Assets.xcassets/checkCaution.imageset/checkCaution.png> <img src=https://raw.githubusercontent.com/young-k/cure/master/Cure/Cure/Assets.xcassets/checkFailed.imageset/checkFailed.png>

</p>

#### Cure front-end
[Check it out Here](https://github.com/young-k/cure "Cure Frontend")

This repo contains the code for the backend that provides information for Cure. Cure was created to allow members of Cornell Appdev to be able to better monitor the status of the servers their apps rely on to function. With timestamped success and failure times, and the ability to graph the results of multiple tests over the course of a day, the team will be able document and react to unexptected server disturbances 24-7. 
 
This backend was built using [Flask](https://flask-sqlalchemy.palletsprojects.com/en/2.x/ ) and [SQLAlchemy](https://www.sqlalchemy.org), and deployed on Google Cloud Servers.

### Run Locally
Activate a python virtual enviroment and install necessary requirements with `pip install -r requirements.txt`. Then run with:
```python app.py```


### Database Design
```
.
└── App
    ├── id
    ├── name
    ├── icon
    ├── test(s)
    │   ├── id
    │   ├── name
    │   ├── url
    │   ├── method
    │   ├── parameters
    │   ├── Result(s)
    │   │   ├── id
    │   │   ├── success
    │   │   ├── createdAt
    │   │   └── updatedAt
    │   ├── createdAt
    │   └── updatedAt
    ├── createdAt
    └── updatedAt
```
The backend has endpoints for posting, retreiving and deletion of Apps, their Tests, and the Results of said tests. 
