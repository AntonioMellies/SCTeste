from flask import jsonify, request ,Blueprint
from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)

# Exceptions
from exceptions.AuthException import AuthException
from exceptions.FormMissingParametersException import FormMissingParametersException

# Models
from models.auth.User import User

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

from main import bcrypt

@auth_blueprint.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username_form = request.json.get('username', None)
    password_form = request.json.get('password', None)

    if not username_form or len(str(username_form).replace(" ", "")) == 0:
        field = {'field': 'username'}
        raise FormMissingParametersException(payload=field, program='login')

    if not password_form or len(str(password_form).replace(" ", "")) == 0:
        field = {'field': 'password'}
        raise FormMissingParametersException(payload=field, program='login')

    user = User.query.filter(User.username ==username_form).first()

    if user is None:
        field = {'error': 'Usuario nao cadastrado'}
        raise AuthException(payload=field, program='login')

    if not bcrypt.check_password_hash(user.password, password_form):
        field = {'error': 'Senha incorreta'}
        raise AuthException(payload=field, program='login')

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200


@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200