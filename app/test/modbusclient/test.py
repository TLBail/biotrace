import unittest
from modules.ModbusClient import ModbusClient
from test.testServer import TestServer
from multiprocessing import Process


class TestModbusClient(unittest.TestCase):

    def setUp(self):
        self.server = TestServer()
        self.server_process = Process(target=self.server.start)
        self.server_process.start()

        self.server_process.join(1)

        self.client = ModbusClient("127.0.0.1", 5001)
        self.client.connect()

    def tearDown(self):
        self.client.disconnect()
        self.server_process.terminate()

    def test_read_signed_short(self):
        data = self.client.read_short('holding', 1001)
        self.assertEqual(data, [-5])

    def test_read_unsigned_short(self):
        data = self.client.read_short('holding', 1001, signed=False)
        self.assertEqual(data, [65531])

    def test_read_signed_int(self):
        data = self.client.read_int('holding', 1000)
        self.assertEqual(data, [2147483643])

    def test_read_unsigned_int(self):
        data = self.client.read_int('holding', 1000)
        self.assertEqual(data, [2147483643])

    def test_read_int_little(self):
        data = self.client.read_int('holding', 1000, endian=1)
        self.assertEqual(data, [-67108993])

    def test_read_float_little(self):
        data = self.client.read_float('input', 2000, endian=1)
        self.assertEqual(round(data[0], 2), -100.79)

    def test_read_float_big(self):
        data = self.client.read_float('input', 2000, endian=0)
        self.assertNotEqual(round(data[0], 2), -100.79)

    def test_read_bool(self):
        data = self.client.read_bool('coils', 2999, 3)
        self.assertEqual(data, [True, False, True])

    def test_read_invalid_address(self):
        with self.assertRaises(Exception):
            self.client.read_short('input', 1001)

    def test_read_invalid_type(self):
        with self.assertRaises(Exception):
            self.client.read_short('invalid', 1001)

    def run_test(self):
        unittest.main()
