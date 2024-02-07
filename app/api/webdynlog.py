from flask import Blueprint, jsonify, request
from modules.Database import Database

bp = Blueprint('webdynlog', __name__, url_prefix='/api')
db = Database()


@bp.route('/webdynlogs', methods=['GET'])
def get_configs():
    global db

    data = db.get_logs()
    json_data = []
    for result in data:
        id = result[0]
        type = result[1]
        name = result[2]
        content = str(result[3]).removeprefix("b'").removesuffix("'")
        date = result[4].strftime('%Y-%m-%d')
        updatedAt = result[5].strftime('%Y-%m-%d')
        deletedAt = result[6].strftime('%Y-%m-%d') if result[6] is not None else None

        json_data.append({'id': id, 'name': name, 'type': type, 'content': content, 'date': date, 'updateAt': updatedAt, 'deleteAt': deletedAt})

    return jsonify(json_data)
