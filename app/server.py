from api.webdynlog import bp as webdynlog_bp
from api.webdynconfig import bp as webdynconfig_bp
from modules.Database import init_engine, init_db, db_session, db_models
from flask import Flask, Blueprint, render_template
from flask_socketio import SocketIO
from sockets.commsocket import commsocket
import rocher
from configparser import ConfigParser
from modules.LogParser import parse_log

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)
socketio = SocketIO(app)

# Enregistrer les événements socket
commsocket(socketio)

# Serve the static files from the Monaco editor
blueprint = Blueprint(
	"monaco", __name__, static_url_path="/static/vs", static_folder=rocher.path()
)
app.register_blueprint(blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mariadb+mariadbconnector://{config['database'].get('username', 'dev')}:{config['database'].get('password', 'dev')}@{config['database'].get('hostname', '127.0.0.1')}:{config['database'].get('port', '3306')}/{config['database'].get('name', 'Biotrace')}"

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
	configs = db_session.query(db_models["File"]).filter(db_models["File"].type == 'config').order_by(db_models["File"].id.desc()).all()
	last_config = configs[0].serialize() if len(configs) > 0 else None

	return render_template('routes/webdynconfig.jinja', configs=[config.serialize() for config in configs], last_config=last_config)


@app.route('/suivilogs')
def suivilogs():
	logs = db_session.query(db_models["File"]).filter(db_models["File"].type == 'log').order_by(db_models["File"].id.desc()).all()

	parsed_log = []
	for log in logs:
		content = parse_log(str(log.content.decode("utf-8")))
		log_parsed = {
			'id': log.id,
			'name': log.name,
			'type': log.type,
			'createdAt': log.created_at.strftime('%Y-%m-%d'),
			'content': content
		}
		parsed_log.append(log_parsed)
		print(log_parsed)

	return render_template('routes/suivilogs.jinja', logs=parsed_log)


@app.route('/pontbascule')
def pontbascule():
	return render_template('routes/pontbascule.jinja')


@app.route('/webdynemul')
def webdynemul():
	return render_template('routes/webdynemul.jinja')


@app.route('/config')
def webdynconfug():
	return render_template('routes/config.jinja')


if __name__ == '__main__':
	socketio.run(app, debug=config['app'].getboolean('debug', False), host='0.0.0.0', port=5000, use_reloader=True, log_output=True)
	app.run(debug=True, host='0.0.0.0', port=5000)
	print("Server running on port 5000")
