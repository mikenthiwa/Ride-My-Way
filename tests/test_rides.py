import unittest
import sys  # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

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


if __name__ == '__main__':
    unittest.main()