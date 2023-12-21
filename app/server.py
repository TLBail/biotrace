from flask import Flask, render_template
from flask_socketio import SocketIO
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


@socketio.on('modbus')
def handle_modbus(message):
    print('received message: ' + message)
    request = json.loads(message)
    print(request['action'])


if __name__ == '__main__':
    socketio.run(app)
    socket = Socket(socketio)

    app.run(debug=True, host='localhost', port=5000)
    print("Server running on port 5000")
