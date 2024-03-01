from flask import Blueprint, jsonify
from modules.Database import db_session, db_models

bp = Blueprint('webdynlog', __name__, url_prefix='/api')


@bp.route('/webdynlogs', methods=['GET'])
def get_logs():
    try:
        logs = db_session.query(db_models["File"]).filter(db_models["File"].type == 'log').order_by(db_models["File"].id.desc()).all()
        return jsonify([log.serialize() for log in logs])
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})
