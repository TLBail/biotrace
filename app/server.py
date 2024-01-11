from flask import Flask, Blueprint, render_template, request
from flask_socketio import SocketIO
from modules.ModbusClient import ModbusClient
from sockets.commsocket import commsocket
import json
import rocher

app = Flask(__name__)
socketio = SocketIO(app)

# Enregistrer les événements socket
commsocket(socketio)


# Serve the static files from the Monaco editor
blueprint = Blueprint(
    "monaco", __name__, static_url_path="/static/vs", static_folder=rocher.path()
)
app.register_blueprint(blueprint)


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
