import unittest
from app.server import *

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.server.main()
