import unittest
import sys  # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

class AdminEndpoint(ConfigTestCase):
    """This class represents admin test cases"""

    def test_get_users(self):
        """Test API can get all users"""

        res = self.client().get('api/v2/admin/users', headers=self.admin_header)
        self.assertEqual(res.status_code, 200)

    def test_get_a_user(self):
        """Test API can get a user"""
        response = self.client().get('/api/v2/admin/users/test_user@gmail.com', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

        # invalid user
        res = self.client().get('/api/v2/admin/users/chris@gmail.com', headers=self.admin_header)
        self.assertIn("email is not available", str(res.data))

    def test_promote_user(self):
        """Test API can promote user"""
        response = self.client().patch('/api/v2/admin/users/test_user@gmail.com', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("user is admin!", str(response.data))

        res = self.client().patch('/api/v2/admin/users/chris_user@gmail.com', headers=self.admin_header)
        self.assertIn("email is not available", str(res.data))


    def test_delete_user(self):
        """Test API can delete user"""

        response = self.client().delete('/api/v2/admin/users/test_user@gmail.com', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("user deleted", str(response.data))

        res = self.client().delete('/api/v2/admin/users/chris_user@gmail.com', headers=self.admin_header)
        self.assertIn("email is not available", str(res.data))

if __name__ == '__main__':
    unittest.main()