import unittest
import sys  # fix import errors
import os
from werkzeug.security import generate_password_hash
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config import ConfigTestCase

class RidesEndpoint(ConfigTestCase):
    """This class represents rides test cases"""

    def test_get_all_rides(self):
        """Test API can get all rides"""

        res = self.client().get('/api/v1/rides')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Syokimau - Nairobi", str(res.data))

    def test_get_ride(self):
        """Test API can get a ride"""

        res = self.client().get('/api/v1/rides/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Syokimau - Nairobi", str(res.data))

    def test_add_ride(self):
        """Test API can add book"""
        ride = {"route": "Komarock-Nairobi", "driver": "Chris", "time": "9:00"}
        res = self.client().post('/api/v1/rides', data=json.dumps(ride), content_type='application/json')
        self.assertIn("Ride has been successfully added", str(res.data))
        self.assertEqual(res.status_code, 201)

    def test_add_ride_without_route(self):
        """Test API cannot add ride with route missing"""
        ride = { "driver": "Chris", "time": "9:00"}
        res = self.client().post('/api/v1/rides', data=json.dumps(ride), content_type='application/json')
        self.assertIn("Route is not provided Missing required parameter in the JSON body", str(res.data))



if __name__ == '__main__':
    unittest.main()