from flask import Flask
from flask_restplus import Api

from instance.config import app_config


def create_app(config_name):
    # Expect token in api_doc

    authorizations = {'apikey': {'type': 'apiKey', 'in': 'header', 'name': 'x-access-token'}}

    # Create flask app

    app = Flask(__name__, instance_relative_config=True)
    # Enable swagger editor
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SWAGGER_UI_JSONEDITOR'] = True
    app.url_map.strict_slashes = False



    api = Api(app=app,
              title='Ride_My_Way',
              authorizations=authorizations,
              version='1.0',
              description='Ride-My-Way is a carpooling application that provides'
                          ' drivers with the ability to create ride'
                          ' offers and passengers to join available ride offers.')

    from resources.rides import api as rides
    api.add_namespace(rides, path='/api/v1')

    from resources.users import api as reg_login
    api.add_namespace(reg_login, path='/api/v1')

    from resources.drivers import api as driver
    api.add_namespace(driver, path='/api/v1')

    return app
