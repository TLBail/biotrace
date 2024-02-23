from flask import Blueprint, jsonify, request
from modules.Database import db_session
from models.file import File

bp = Blueprint('webdynconfig', __name__, url_prefix='/api')


@bp.route('/webdynconfigs', methods=['GET'])
def get_configs():
    try:
        configs = db_session.query(File).filter(File.type == 'config').order_by(File.id.desc()).all()
        return jsonify([c.serialize() for c in configs])
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})


@bp.route('/webdynconfigs', methods=['POST'])
def add_config():
    try:
        name = request.json['name']
        content = request.json['content']

        config = File(name, 'config', content)

        db_session.add(config)
        db_session.commit()

        return jsonify(config.serialize())
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})
