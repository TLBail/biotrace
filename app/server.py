from flask import Flask, render_template, request
from flask_socketio import SocketIO
from modules.ModbusClient import ModbusClient
from sockets.commsocket import commsocket
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Enregistrer les événements socket
commsocket(socketio)


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





if __name__ == '__main__':
    socketio.run(app)
    app.run(debug=True, host='localhost', port=5000)
    print("Server running on port 5000")
