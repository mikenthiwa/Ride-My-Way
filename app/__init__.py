# app/__init__.py

from flask import Flask, request
from flask_restplus import Api
import psycopg2

from instance.config import app_config, config


def create_app(config_name):
    # Expect token in api_doc
    authorizations = {'apikey': {'type': 'apiKey', 'in': 'header', 'name': 'x-access-token'}}

    # Create flask app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.url_map.strict_slashes = False

    # Enable swagger editor
    app.config['SWAGGER_UI_JSONEDITOR'] = True

    api = Api(app=app,
              title='Ride_My_Way',
              authorizations=authorizations,
              version='3.0',
              doc='/api/v3/documentation',
              description='Ride-My-Way is a carpooling application that provides'
                          ' drivers with the ability to create ride'
                          ' offers and passengers to join available ride offers.')


    from resources.rides import api as rides
    api.add_namespace(rides, path='/api/v3')

    from resources.signup_login import api as reg_login
    api.add_namespace(reg_login, path='/api/v3')

    from resources.drivers import api as driver
    api.add_namespace(driver, path='/api/v3')

    from resources.admin import api as admin
    api.add_namespace(admin, path='/api/v3')

    from resources.users import api as users
    api.add_namespace(users, path='/api/v3')

    return app

# def connect():
#     """ Connect to the PostgreSQL database server """
#     conn = None
#     try:
#         # read connection parameters
#         params = config()
#
#         # connect to the PostgreSQL server
#         print('Connecting to the PostgreSQL database...')
#         conn = psycopg2.connect(**params)
#
#         # create a cursor
#         cur = conn.cursor()
#
#         # execute a statement
#         print('PostgreSQL database version:')
#         cur.execute('SELECT version()')
#
#         # display the PostgreSQL database server version
#         db_version = cur.fetchone()
#         print(db_version)
#
#         # close the communication with the PostgreSQL
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')
