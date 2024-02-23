from flask import Blueprint, jsonify
from modules.Database import db_session
from models.file import File

bp = Blueprint('webdynlog', __name__, url_prefix='/api')

@bp.route('/webdynlogs', methods=['GET'])
def get_logs():
	logs = db.session.execute(db.select([db.File]).where(db.File.type == 'log').order_by(db.File.id.desc()).limit(10))
	
	print(logs)
	
	return jsonify([])