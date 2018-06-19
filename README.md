# Ride-My-Way

Ride-my App(apiv1) is a carpooling api that provides drivers with the ability to create ride offers and passengers  to join available ride offers.

## Getting Started

Go to https://github.com/mikenthiwa/Ride-My-Way/apiv1.<br/>
Download or clone the repository to your local machine.<br/>
Open the project using your ide

## Prerequisites

* Python 3 and above.
* Virtual environment.
* Flask
* flask-restplus
* Postman
* Browser e.g Chrome, firefox, safari

## Installing

#### Virtual environment

* On the root directory folder, open cmd.
* Run the command: virtualenv venv,  to create a virtual <br/>
 environment with the name venv. Folder with the name venv will <br>
 created.
* Activate the virtual environment by moving to <br>
to the Script directory i.e. cd venv\Scripts, and running <br>
activate.

### Application requirements

The requirements.txt files will contain all the requirements needed 
for the application. <br>
To install the requirements, simply run in cmd: pip install -r requirements.txt <br/>
Ensure you are located within the root directory and your virtual env. is activated <br/>
Some of the third party modules that will be installed are: 
* flask - Python module used for building web application.
* flask-restplus - flask extension used for developing API.
* Coverage - Python module used in testing, for assessing the quantity of test covered.
* Pytest - Python module for running test.

### Postman
Application used for testing endpoint.

|Requests     |   EndPoint                      | Functionality
|:-----------:|:-------------------------------:|:--------------:
   GET        |   api/v1/rides                  | Get all Rides 
   GET        |  api/vi/rides/{rideId}          | Get a specific ride                   
   POST       |  api/v1/driver/rides            | Add a ride                  
   POST       |  api/v1/rides/{rideId}/Request  | Request to join a ride                     





    
 
