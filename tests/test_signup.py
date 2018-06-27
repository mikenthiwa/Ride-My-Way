import unittest
import sys  # fix import errors
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

class SignUpEndpoint(ConfigTestCase):
    """This class represents sign up test case"""






if __name__ == '__main__':
    unittest.main()