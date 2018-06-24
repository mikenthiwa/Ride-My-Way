import unittest
import sys  # fix import errors
import os
import json
from werkzeug.security import generate_password_hash
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, db
from app.models import Rides, Users

class ConfigTestCase(unittest.TestCase):
    """This class represents the base configurations for all tests"""

    def setUp(self):
        """Define test variables and initialize app"""

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables

            db.create_all()

            test_route_1 = Rides(route="Syokimau - Nairobi", driver="Regina", time="12:00")
            test_route_2 = Rides(route="Nairobi - Limuru", driver="Kimani", time="12:00")
            test_user = Users(email="test_user@gmail.com", username="test_user", password=generate_password_hash("123456789", method='sha256'))
            test_driver = Users(email="test_driver@gmail.com", username="test_driver", password=generate_password_hash("123456789"), is_driver=True)
            test_admin = Users(email="admin@admin.com", username="admin", password=generate_password_hash("123456789"), is_admin=True)
            db.session.add(test_user)
            db.session.add(test_driver)
            db.session.add(test_admin)
            db.session.add(test_route_1)
            db.session.add(test_route_2)
            db.session.commit()

            test_user_cred = {"email": "test_user@gmail.com", "password": "123456789"}
            test_driver_cred = {"email": "test_driver@gmail.com", "password": "123456789"}
            test_admin_cred = {"email": "admin@admin.com", "password": "123456789"}


            user_response = self.client().post('/api/v2/login', data=json.dumps(test_user_cred),
                                               content_type='application/json')
            driver_response = self.client().post('/api/v2/login', data=json.dumps(test_driver_cred),
                                               content_type='application/json')
            admin_response = self.client().post('/api/v2/login', data=json.dumps(test_admin_cred),
                                               content_type='application/json')

            self.user_token_dict = json.loads(user_response.get_data(as_text=True))
            driver_token_dict = json.loads(driver_response.get_data(as_text=True))
            admin_token_dict = json.loads(admin_response.get_data(as_text=True))

            user_token = self.user_token_dict["token"]
            driver_token = driver_token_dict["token"]
            admin_token = admin_token_dict["token"]

            self.user_header = {"Content-Type": "application/json", "x-access-token": user_token}
            self.driver_header = {"Content-Type": "application/json", "x-access-token": driver_token}
            self.admin_header = {"Content-Type": "application/json", "x-access-token": admin_token}


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
