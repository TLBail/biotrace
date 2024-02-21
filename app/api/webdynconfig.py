from flask import Blueprint, jsonify, request

bp = Blueprint('webdynconfig', __name__, url_prefix='/api')


@bp.route('/webdynconfigs', methods=['GET'])
def get_configs():
    return jsonify([])


# @bp.route('/webdynconfigs', methods=['POST'])
# def add_config():
#     global db

#     # get body

#     name = request.json['name']
#     content = request.json['content']

#     try:
#         db.add_config(name, content)
#         return jsonify({'status': 'success'})
#     except Exception as e:
#         return jsonify({'status': 'error', 'error': str(e)})
