from modules.LogParser import parse_log
import unittest


class TestLogParser(unittest.TestCase):

    def setUp(self):
        with open("app/test/logs/samples/BDLV_240308_000001.log") as file:
            self.log = file.read()

        self.logs = parse_log(self.log)

    def test_size(self):
        self.assertEqual(len(self.logs), 6)

    def run_test(self):
        unittest.main()
