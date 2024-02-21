from flask import Flask, Blueprint, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import database_exists, create_database
from sockets.commsocket import commsocket
import rocher

from api.webdynconfig import bp as webdynconfig_bp
from api.webdynlog import bp as webdynlog_bp

app = Flask(__name__)
socketio = SocketIO(app)

# Enregistrer les événements socket
commsocket(socketio)

app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://dev:dev@127.0.0.1:3306/Biotrace"

# Models de la BDD
from models.File import db

db.init_app(app)
with app.app_context():
	if not database_exists(db.engine.url): create_database(db.engine.url)
	db.create_all()

# Serve the static files from the Monaco editor
blueprint = Blueprint(
    "monaco", __name__, static_url_path="/static/vs", static_folder=rocher.path()
)
app.register_blueprint(blueprint)

# Register the API blueprint
app.register_blueprint(webdynconfig_bp)
app.register_blueprint(webdynlog_bp)


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
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=True, log_output=True)
    app.run(debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
    print("Server running on port 5000")