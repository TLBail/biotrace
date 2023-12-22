from flask import Flask, render_template, request
from flask_socketio import SocketIO
from modules.ModbusClient import ModbusClient
import json

app = Flask(__name__)
socketio = SocketIO(app)

rooms = {}


@app.route('/')
@app.route('/testcomm')
def testcomm():
    return render_template('routes/testcomm.html')


@app.route('/webdynconfig')
def webdynconfig():
    return render_template('routes/webdynconfig.html')


@app.route('/suivilogs')
def suivilogs():
    return render_template('routes/suivilogs.html')


@app.route('/pontbascule')
def pontbascule():
    return render_template('routes/pontbascule.html')


@app.route('/webdynemul')
def webdynemul():
    return render_template('routes/webdynemul.html')


@app.route('/config')
def config():
    return render_template('routes/config.html')


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
            socketio.emit('modbus', json.dumps({'action': 'connect', 'status': True, 'data': f"Connected to {ip}:{port}"}))
        else:
            socketio.emit('modbus', json.dumps({'action': 'connect', 'status': False, 'data': f"Failed to connect to {ip}:{port}"}))

    elif action == 'disconnect':
        if (isinstance(rooms[request.sid], ModbusClient)):
            rooms[request.sid].disconnect()
            rooms[request.sid] = None
            socketio.emit('modbus', json.dumps({'action': 'disconnect', 'status': True, 'data': "Disconnected"}))
        else:
            socketio.emit('modbus', json.dumps({'action': 'disconnect', 'status': False, 'data': "Not connected"}))

    elif action == 'read':
        if (not isinstance(rooms[request.sid], ModbusClient)):
            socketio.emit('modbus', json.dumps({'action': 'read', 'status': False, 'data': "Not connected"}))
        else:
            type_register = payload['type']
            address = payload['address']
            count = payload['count']

            if type_register == 'coil':
                data = rooms[request.sid].read_coils(address, count)
            elif type_register == 'discrete':
                data = rooms[request.sid].read_discrete_inputs(address, count)
            elif type_register == 'input':
                data = rooms[request.sid].read_input_registers(address, count)
            elif type_register == 'holding':
                data = rooms[request.sid].read_holding_registers(address, count)
            else:
                socketio.emit('modbus', json.dumps({'action': 'read', 'status': False, 'data': "Unknown type"}))

            socketio.emit('modbus', json.dumps({'action': 'read', 'status': True, 'type': type_register, 'address': address, 'count': count, 'data': data}))


if __name__ == '__main__':
    socketio.run(app)
    app.run(debug=True, host='localhost', port=5000)
    print("Server running on port 5000")
