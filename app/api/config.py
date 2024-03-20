from flask import Blueprint, jsonify, request
from configparser import ConfigParser


bp = Blueprint('config', __name__, url_prefix='/api')

config = ConfigParser()
config.read('config.ini')


@bp.route('/config/ftp', methods=['POST'])
def add_ftpconfig():
    username = request.json['username']
    password = request.json['password']
    hostname = request.json['hostname']
    port = request.json['port']

    config['ftp'] = {
        'hostname': str(hostname),
        'username': str(username),
        'password': str(password),
        'port': int(port)
    }

    try:
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})


@bp.route('/config/webdynconfig', methods=['POST'])
def add_webdynconfig():
    save_frequency = request.json['save_frequency']
    nb_files = request.json['nb_files']
    file_retention_period = request.json['file_retention_period']

    config['webdynconfig'] = {
        'save_frequency': int(save_frequency),
        'nb_files': int(nb_files),
        'file_retention_period': int(file_retention_period),
    }

    try:
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})


@bp.route('/config/logconfig', methods=['POST'])
def add_logconfig():

    file_retention_period = request.json['file_retention_period']

    config['logconfig'] = {
        'file_retention_period': int(file_retention_period),
    }

    try:
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})
