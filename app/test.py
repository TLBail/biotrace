from test.modbusclient.test import TestModbusClient
from test.logs.test import TestLogParser

if __name__ == '__main__':
    mc = TestModbusClient()
    mc.run_test()

    lp = TestLogParser()
    lp.run_test()
