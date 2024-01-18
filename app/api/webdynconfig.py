from flask import Blueprint, jsonify, request
from modules.Database import Database

bp = Blueprint('webdynconfig', __name__, url_prefix='/api')
db = Database()


@bp.route('/webdynconfigs', methods=['GET'])
def get_configs():
    global db

    data = db.get_configs(10)
    json_data = []
    for result in data:
        id = result[0]
        type = result[1]
        name = result[2]
        content = str(result[3]).removeprefix("b'").removesuffix("'")
        date = result[4].strftime('%Y-%m-%d')
        updateAt = result[5].strftime('%Y-%m-%d')
        deletteAt = result[6].strftime('%Y-%m-%d') if result[6] is not None else None

        json_data.append({'id': id, 'name': name, 'type': type, 'content': content, 'date': date, 'updateAt': updateAt, 'deletteAt': deletteAt})

    return jsonify(json_data)


@bp.route('/webdynconfigs', methods=['POST'])
def add_config():
    global db

    # get body

    name = request.json['name']
    content = request.json['content']

    try:
        db.add_config(name, content)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)})
