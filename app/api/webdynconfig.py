from flask import Blueprint, jsonify
from modules.Database import Database

bp = Blueprint('webdynconfig', __name__, url_prefix='/api')
db = Database()


@bp.route('/webdynconfigs', methods=['GET'])
def get_configs():
    global db

    data = db.get_configs(10)
    json_data = []
    for result in data:
        json_data.append({'id': result[0], 'name': result[1], 'type': result[2], 'content': str(result[3]), 'date': result[4].strftime('%Y-%m-%d'), 'updateAt': result[5].strftime('%Y-%m-%d'), 'deletteAt': result[6].strftime('%Y-%m-%d') if result[6] != None else None})

    return jsonify(json_data)
