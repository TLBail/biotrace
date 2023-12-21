from pymodbus.client.tcp import ModbusTcpClient

class ModbusClient:

    def __init__(self, ip='127.0.0.1', port=502):
        self.ip = ip
        self.port = port
        self.client = ModbusTcpClient(self.ip, port=self.port, auto_open=False)

    def connect(self):
        return self.client.connect()

    def disconnect(self):
        return self.client.close()

    def read_holding_registers(self, address, count):
        if not self.client.is_socket_open():
            return False
        return self.client.read_holding_registers(address=address, count=count).registers

    def read_input_registers(self, address, count):
        if not self.client.is_socket_open():
            return False
        return self.client.read_input_registers(address=address, count=count).registers

    def read_coils(self, address, count):
        if not self.client.is_socket_open():
            return False
        return self.client.read_coils(address=address, count=count).registers

    def read_discrete_inputs(self, address, count):
        if not self.client.is_socket_open():
            return False
        return self.client.read_discrete_inputs(address=address, count=count).registers
