from pymodbus.client.tcp import ModbusTcpClient
from modules.Utils import hex_to_float, hex_to_int, hex_to_double
import math


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
        try:
            if not self.client.is_socket_open():
                raise Exception("Connection closed")

            data = self.client.read_holding_registers(address=address, count=count).registers

            if not data:
                raise Exception(f"No data at address {address}")

            return data

        except Exception as e:
            raise e

    def read_input_registers(self, address, count):
        try:
            if not self.client.is_socket_open():
                raise Exception("Connection closed")

            data = self.client.read_input_registers(address=address, count=count).registers

            if not data:
                raise Exception(f"No data at address {address}")

            return data

        except Exception as e:
            raise e

    def read_coils(self, address, count):
        try:
            if not self.client.is_socket_open():
                raise Exception("Connection closed")

            data = self.client.read_coils(address=address, count=count).bits

            if not data:
                raise Exception(f"No data at address {address}")

            return data

        except Exception as e:
            raise e

    def read_discrete_inputs(self, address, count):
        try:
            if not self.client.is_socket_open():
                raise Exception("Connection closed")

            data = self.client.read_discrete_inputs(address=address, count=count).bits

            if not data:
                raise Exception(f"No data at address {address}")

            return data

        except Exception as e:
            raise e

    def read_register(self, register, address, count):
        if register == 'holding':
            return self.read_holding_registers(address, count)
        elif register == 'input':
            return self.read_input_registers(address, count)
        elif register == 'coils':
            return self.read_coils(address, count)
        elif register == 'discrete':
            return self.read_discrete_inputs(address, count)
        else:
            raise Exception("Invalid register")

    def read_short(self, register, addr, signed=True, count=1):
        result = self.read_register(register, addr, count)

        if signed:
            signed_values = [val if val < 32768 else val - 65536 for val in result]
            return signed_values

        return result

    def read_int(self, register, addr, endian=0, signed=True, count=1):
        result = self.read_register(register, addr, count * 2)

        int_values = [hex_to_int(result[i], result[i + 1], endian) for i in range(0, len(result), 2)]

        if signed:
            signed_values = [val if val < 2147483648 else val - 4294967296 for val in int_values]
            return signed_values

        return int_values

    def read_float(self, register, addr, endian=0, count=1):
        try:
            result = self.read_register(register, addr, count * 2)
        except Exception as e:
            raise e

        float_values = []
        for i in range(0, len(result), 2):
            v = hex_to_float(result[i], result[i + 1], endian)

            if math.isnan(v):
                float_values.append(0.0)
                break

            float_values.append(v)

        if not float_values:
            raise Exception(f"No float data at address {addr}")

        return float_values

    def read_double(self, register, addr, endian=0, count=1):
        result = self.read_register(register, addr, count * 4)

        double_values = []

        for i in range(0, len(result), 4):
            v = hex_to_double(result[i], result[i + 1], result[i + 2], result[i + 3], endian)

            if math.isnan(v):
                double_values.append(0.0)
                break

            double_values.append(v)

        if not double_values:
            raise Exception(f"No double data at address {addr}")

        return double_values

    def read_bool(self, register, addr, count=1):
        result = self.read_register(register, addr, count)

        bool_values = [bool(v) for k, v in enumerate(result) if k < count]
        return bool_values

    def read(self, type, register, addr, endian=0, signed=True, count=1):
        if type == "short":
            return self.read_short(register, addr, signed, count)
        elif type == "int":
            return self.read_int(register, addr, endian, signed, count)
        elif type == "float":
            return self.read_float(register, addr, endian, count)
        elif type == "double":
            return self.read_double(register, addr, endian, count)
        elif type == "boolean":
            return self.read_bool(register, addr, count)
        else:
            raise Exception("Invalid type")
