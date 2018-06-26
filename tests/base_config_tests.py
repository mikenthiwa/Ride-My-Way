import unittest
import sys  # fix import errors
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from app.models import Rides, Users

class ConfigTestCase(unittest.TestCase):
    """This class represents the base configurations for all tests"""

    def setUp(self):
        """Define test variables and initialize app"""

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        ride = Rides()
        user = Users()

        ride.add_ride("Syokimau - Nairobi", "Regina", "12:00")
        ride.add_ride("Nairobi - Limuru", "Regina", "12:00")
        user.add_users("test_user@gmail.com", "test_user", "123456789")
        user.add_users("test_driver@gmail.com", "test_driver", "123456789", driver=True)
        user.add_users("admin@admin.com", "admin", "123456789", admin=True)

        test_user_cred = {"email": "test_user@gmail.com", "password": "123456789"}
        test_driver_cred = {"email": "test_driver@gmail.com", "password": "123456789"}
        test_admin_cred = {"email": "admin@admin.com", "password": "123456789"}

        user_response = self.client().post('/api/v1/login', data=json.dumps(test_user_cred),
                                           content_type='application/json')
        driver_response = self.client().post('/api/v1/login', data=json.dumps(test_driver_cred),
                                           content_type='application/json')
        admin_response = self.client().post('/api/v1/login', data=json.dumps(test_admin_cred),
                                           content_type='application/json')

        user_token_dict = json.loads(user_response.get_data(as_text=True))
        driver_token_dict = json.loads(driver_response.get_data(as_text=True))
        admin_token_dict = json.loads(admin_response.get_data(as_text=True))

        user_token = user_token_dict["token"]
        driver_token = driver_token_dict["token"]
        admin_token = admin_token_dict["token"]


        self.user_header = {"Content-Type": "application/json", "x-access-token": user_token}
        self.driver_header = {"Content-Type": "application/json", "x-access-token": driver_token}
        self.admin_header = {"Content-Type": "application/json", "x-access-token": admin_token}



if __name__ == '__main__':
    unittest.main()
