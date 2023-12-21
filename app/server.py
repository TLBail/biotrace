from flask import Flask, render_template
from flask_socketio import SocketIO
from modules.ModbusClient import ModbusClient
import json

app = Flask(__name__)
socketio = SocketIO(app)


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


modbusClient = None


@socketio.on('modbus')
def handle_modbus(message):
    global modbusClient

    request = json.loads(message)
    action = request['action']

    if action == 'connect':
        ip = request['ip']
        port = request['port']
        if (isinstance(modbusClient, ModbusClient)):
            modbusClient.disconnect()
        modbusClient = ModbusClient(ip=ip, port=port)

        if modbusClient.connect():
            socketio.emit('modbus', json.dumps({'action': 'connect', 'status': True, 'data': f"Connected to {ip}:{port}"}))
        else:
            socketio.emit('modbus', json.dumps({'action': 'connect', 'status': False, 'data': f"Failed to connect to {ip}:{port}"}))

    elif action == 'disconnect':
        if (isinstance(modbusClient, ModbusClient)):
            modbusClient.disconnect()
            modbusClient = None
            socketio.emit('modbus', json.dumps({'action': 'disconnect', 'status': True, 'data': "Disconnected"}))
        else:
            socketio.emit('modbus', json.dumps({'action': 'disconnect', 'status': False, 'data': "Not connected"}))

    elif action == 'read':
        if (not isinstance(modbusClient, ModbusClient)):
            socketio.emit('modbus', json.dumps({'action': 'read', 'status': False, 'data': "Not connected"}))
        else:
            type_register = request['type']
            address = request['address']
            count = request['count']

            if type_register == 'coil':
                data = modbusClient.read_coils(address, count)
            elif type_register == 'discrete':
                data = modbusClient.read_discrete_inputs(address, count)
            elif type_register == 'input':
                data = modbusClient.read_input_registers(address, count)
            elif type_register == 'holding':
                data = modbusClient.read_holding_registers(address, count)
            else:
                socketio.emit('modbus', json.dumps({'action': 'read', 'status': False, 'data': "Unknown type"}))

            socketio.emit('modbus', json.dumps({'action': 'read', 'status': True, 'type': type_register, 'address': address, 'count': count, 'data': data}))


if __name__ == '__main__':
    socketio.run(app)
    app.run(debug=True, host='localhost', port=5000)
    print("Server running on port 5000")
