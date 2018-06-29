[![Build Status](https://travis-ci.org/mikenthiwa/Ride-My-Way.svg?branch=master)](https://travis-ci.org/mikenthiwa/Ride-My-Way)
[![Coverage Status](https://coveralls.io/repos/github/mikenthiwa/Ride-My-Way/badge.svg?branch=apiv1)](https://coveralls.io/github/mikenthiwa/Ride-My-Way?branch=apiv1)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Ride-My-Way

Ride-my App(apiv3) is a carpooling api that provides drivers with the ability to create ride offers and passengers  to join available ride offers.

***

![Home Image](https://raw.github.com/mikenthiwa/Ride-My-Way/apiv1/img.png)

## Getting Started
```
Go to https://github.com/mikenthiwa/Ride-My-Way.git 
Download or clone the repository to your local machine. 
Open the project using your ide
```

***

## Prerequisites

* Python 3 and above.
* Virtual environment.
* Flask
* flask-restplus
* Postman
* Browser e.g Chrome, firefox, safari

***

## Installing

#### Creating virtual environment

On the root directory folder, open cmd.
````
* Run the command: virtualenv venv
* Activating virtual environment : cd venv\Scripts: activate 
````

***
### Application requirements

The requirements.txt files will contain all the requirements needed 
for the application. <br>
To install the requirements :
````
pip install -r requirements.txt 
````

***
Ensure you are located within the root directory and your virtual env. is activated <br/>
Some of the third party modules that will be installed are: 
* flask - Python module used for building web application.
* flask-restplus - flask extension used for developing API.
* Coverage - Python module used in testing, for assessing the quantity of test covered.
* Pytest - Python module for running test.

***

### Postman
Application used for testing endpoint. <br>
Endpoint available for this api are shown in the table below:
````

|Requests     |   EndPoint                           | Functionality
|:-----------:|:-------------------------------------:--------------:
   GET        |  /api/v1/rides                       | Get all Rides 
   GET        |  /api/vi/rides/{rideId}              | Get a specific ride
   DELETE     |  /api/v1/driver/rideId               | Delete ride          
   POST       |  /api/v1/driver/rides                | Add a ride                  
   PATCH      |  /api/v1/rides/{rideId}/Request      | Request to join a ride
   PATCH      |  /api/v1/driver/rides/rideId/Accept  | Accept the request passengers request
   PUT        |  /api/vi/driver/rides/rideId         | Modify ride details
   POST       |  /api/v1/register                    | Register users
   POST       |  /api/v1/login                       | Login user
   PUT        |  /api/v1/auth/user/email             | Reset password
   PUT        |  /api/vi/auth/user/email             | Reset username                       
   GET        |  /api/v1/admin/users                 | Get all users
   PATCH      |  /api/v1/admin/users/<int:user_id>   | Promote users
````

***

## Running test
````
coverage run -m unittest
pytest
````
***

## Built using

* python 3.6.5
* Flask
* flask-restplus

***

## Heroku

https://ridemywayapiv1.herokuapp.com/api/v1/documentation
***

## Versioning
Most recent version: version 1

***

## Authors
Michael Mutua 

***

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration and encouragement
* etc

***
    
 
