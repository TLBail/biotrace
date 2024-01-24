from pymodbus.client.tcp import ModbusTcpClient
from modules.Utils import hex_to_float


class ModbusClient:

    def __init__(self, ip='127.0.0.1', port=502):
        self.ip = ip
        self.port = port
        self.client = ModbusTcpClient(self.ip, port=self.port, auto_open=False)

    def connect(self):
        return self.client.connect()

    def disconnect(self):
        return self.client.close()

    def read_holding_registers(self, address, count, value_type, invert, signed):
        if not self.client.is_socket_open():
            return False
        value = self.client.read_holding_registers(address=address, count=count).registers
        if value_type == 'float':
            value = hex_to_float(value[0], value[1], invert)
        elif value_type == 'int':
            if signed:
                print(value)
                # for each value
                for i in range(count):
                    # if value is greater than 32767, then it is a negative value
                    value[i] = value[i] - 65536 if value[i] > 32767 else value[i]
        return value

    def read_input_registers(self, address, count, value_type, invert, signed):
        if not self.client.is_socket_open():
            return False
        value = self.client.read_input_registers(address=address, count=count).registers
        if value_type == 'float':
            value = hex_to_float(value[0], value[1], invert)
        elif value_type == 'int':
            if signed:
                print(value)
                # for each value
                for i in range(count):
                    # if value is greater than 32767, then it is a negative value
                    value[i] = value[i] - 65536 if value[i] > 32767 else value[i]
        return value

    def read_coils(self, address, count):
        if not self.client.is_socket_open():
            return False
        return self.client.read_coils(address=address, count=count).bits

    def read_discrete_inputs(self, address, count):
        if not self.client.is_socket_open():
            return False
        return self.client.read_discrete_inputs(address=address, count=count).registers
