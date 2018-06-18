import unittest
import sys  # fix import errors
import os
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


if __name__ == '__main__':
    unittest.main()
