from flask import Flask, Blueprint, render_template
from flask_socketio import SocketIO
from sockets.commsocket import commsocket
import rocher
import os

from api.webdynconfig import bp as webdynconfig_bp
from api.webdynlog import bp as webdynlog_bp
from modules.Database import init_engine, init_db, db_session
from models.File import File

app = Flask(__name__)
socketio = SocketIO(app)

# Enregistrer les événements socket
commsocket(socketio)

# Serve the static files from the Monaco editor
blueprint = Blueprint(
	"monaco", __name__, static_url_path="/static/vs", static_folder=rocher.path()
)
app.register_blueprint(blueprint)

# Register the API blueprint
user = os.getenv('DB_USER', 'dev')
password = os.getenv('DB_PASSWORD', 'dev')
host = os.getenv('DB_HOST', 'localhost')
port = int(os.getenv('DB_PORT', '3306'))
database = os.getenv('DB_DATABASE', 'Biotrace')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mariadb+mariadbconnector://{user}:{password}@{host}:{port}/{database}'

init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
init_db()

app.register_blueprint(webdynconfig_bp)
app.register_blueprint(webdynlog_bp)


@app.route('/')
@app.route('/testcomm')
def testcomm():
	return render_template('routes/testcomm.jinja')


@app.route('/webdynconfig')
def webdynconfig():
	configs = db_session.query(File).filter(File.type == 'config').order_by(File.id.desc()).all()
	last_config = configs[0].serialize() if len(configs) > 0 else None

	return render_template('routes/webdynconfig.jinja', configs=[config.serialize() for config in configs], last_config=last_config)


@app.route('/suivilogs')
def suivilogs():
	return render_template('routes/suivilogs.jinja')


@app.route('/pontbascule')
def pontbascule():
	return render_template('routes/pontbascule.jinja')


@app.route('/webdynemul')
def webdynemul():
	return render_template('routes/webdynemul.jinja')


@app.route('/config')
def config():
	return render_template('routes/config.jinja')


if __name__ == '__main__':
	socketio.run(app, debug=True, host='0.0.0.0', port=5000)
	app.run(debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
	print("Server running on port 5000")
