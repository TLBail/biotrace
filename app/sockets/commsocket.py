from flask_socketio import SocketIO
from flask import request
from modules.ModbusClient import ModbusClient
import json


rooms = {}


def commsocket(socketio: SocketIO):

    @socketio.on('connect')
    def handle_connect():
        global rooms
        rooms[request.sid] = None
        print(f"Client {request.sid} connected")

    @socketio.on('disconnect')
    def handle_disconnect():
        global rooms
        del rooms[request.sid]
        print(f"Client {request.sid} disconnected")

    @socketio.on('modbus')
    def handle_modbus(message):
        global rooms
        payload = json.loads(message)
        action = payload['action']

        if action == 'connect':
            ip = payload['ip']
            port = payload['port']
            if (isinstance(rooms[request.sid], ModbusClient)):
                rooms[request.sid].disconnect()
            rooms[request.sid] = ModbusClient(ip=ip, port=port)

            if rooms[request.sid].connect():
                socketio.emit('modbus', json.dumps({'action': 'connect', 'status': True, 'data': f"Connected to {ip}:{port}"}), to=request.sid)
            else:
                socketio.emit('modbus', json.dumps({'action': 'connect', 'status': False, 'data': f"Failed to connect to {ip}:{port}"}), to=request.sid)

        elif action == 'disconnect':
            if (isinstance(rooms[request.sid], ModbusClient)):
                rooms[request.sid].disconnect()
                rooms[request.sid] = None
                socketio.emit('modbus', json.dumps({'action': 'disconnect', 'status': True, 'data': "Disconnected"}), to=request.sid)
            else:
                socketio.emit('modbus', json.dumps({'action': 'disconnect', 'status': False, 'data': "Not connected"}), to=request.sid)

        elif action == 'read':
            if (not isinstance(rooms[request.sid], ModbusClient)):
                socketio.emit('modbus', json.dumps({'action': 'read', 'status': False, 'data': "Not connected"}), to=request.sid)
            else:
                type_register = payload['type']
                address = payload['address']
                count = payload['count']
                value_type = payload['value_type']
                invert = payload['invert']
                signed = payload['signed']

                client = rooms[request.sid]

                try:
                    data = client.read(register=type_register, type=value_type, addr=address, endian=invert, signed=signed, count=count)
                except Exception as e:
                    socketio.emit('modbus', json.dumps({'action': 'read', 'status': False, 'data': str(e)}), to=request.sid)
                    return

                socketio.emit('modbus', json.dumps({'action': 'read', 'status': True, 'type': type_register, 'address': address, 'count': count, 'data': data, 'value_type': value_type, 'invert': invert, 'signed': signed}), to=request.sid)
