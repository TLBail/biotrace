from flask import Blueprint, jsonify
from modules.Database import db_session
from models.file import File

bp = Blueprint('webdynlog', __name__, url_prefix='/api')


@bp.route('/webdynlogs', methods=['GET'])
def get_logs():
    try:
        logs = db_session.query(File).filter(File.type == 'log').order_by(File.id.desc()).all()
        return jsonify([log.serialize() for log in logs])
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})
