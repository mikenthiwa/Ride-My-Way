import unittest
import sys  # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.base_config_tests import ConfigTestCase

class AdminEndpoint(ConfigTestCase):
    """This class represents admin test cases"""


if __name__ == '__main__':
    unittest.main()