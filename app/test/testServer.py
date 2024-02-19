import random
import logging
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server.async_io import StartTcpServer


class TestServer:

    def __init__(self):
            # Enable logging (makes it easier to debug if something goes wrong)
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)

        # Define the Modbus registers
        coils = ModbusSequentialDataBlock(3000, [False] *100)
        discrete_inputs = ModbusSequentialDataBlock(1, [False] * 100)
        holding_registers = ModbusSequentialDataBlock(1001, [0] * 100)
        input_registers = ModbusSequentialDataBlock(2001, [0] * 100)


        # Int values 32 bits so 2 registers
        # [2147483643] -> big endian, [-67108993] -> little endian
        # 1st register = 1000

        # Short values 16 bits so 1 register
        # [32768, 65531] -> Unsigned 16 bits
        # [32768, -5] -> Signed 16 bits
        # 1st register = 1000
        # 2nd register = 1001
        holding_registers.setValues(1, [32767,65531, 16453, 4045, 13736, 22649])

        # float values 32 bits so 2 registers
        # [-100.79, 273.18]
        # 1st register = 2000
        # 2nd register = 2002
        input_registers.setValues(1, [31636, 51650, 2711, 34883])

        # double value 64 bits so 4 registers
        # [42.12345]
        #holding_registers.setValues(3, [16453, 4045, 13736, 22649])

        coils.setValues(1, [True, False, True])


        # Define the Modbus slave context
        slave_context = ModbusSlaveContext(
            di=discrete_inputs,
            co=coils,
            hr=holding_registers,
            ir=input_registers
        )

        # Define the Modbus server context
        self.server_context = ModbusServerContext(slaves=slave_context, single=True)

    def start(self,out=True, ip="localhost", port=5001):
        # Start the Modbus TCP server
        StartTcpServer(context=self.server_context, address=(ip, port))

if __name__ == "__main__":
    server = TestServer()
    server.start()
