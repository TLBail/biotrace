from flask import Blueprint, jsonify, request
from configparser import ConfigParser


bp = Blueprint('config', __name__, url_prefix='/api')

config = ConfigParser()
config.read('config.ini')


@bp.route('/config', methods=['POST'])
def add_config():
    username = request.json['username']
    password = request.json['password']
    hostname = request.json['hostname']
    port = request.json['port']

    config['ftp'] = {
        'hostname': hostname,
        'username': username,
        'password': password,
        'port': port
    }

    try:
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})
