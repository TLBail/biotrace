from flask import Blueprint, jsonify, request

bp = Blueprint('webdynlog', __name__, url_prefix='/api')

@bp.route('/webdynlogs', methods=['GET'])
def get_logs():
	logs = db.session.execute(db.select([db.File]).where(db.File.type == 'log').order_by(db.File.id.desc()).limit(10))
	
	print(logs)
	
	return jsonify([])