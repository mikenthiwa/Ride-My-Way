import unittest
import sys  # fix import errors
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

class AdminEndpoint(ConfigTestCase):
    """This class represents admin test cases"""

    def test_get_users(self):
        """Test API can get all users"""

        res = self.client().get('api/v1/admin/users', headers=self.admin_header)
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()