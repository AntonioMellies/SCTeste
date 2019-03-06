from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (JWTManager)
from utils import Environment

# Blueprints Modules
from auth.auth import auth_blueprint
from system_A.system_a import system_a_blueprint
from system_B.system_b import system_b_blueprint
from system_C.system_c import system_c_blueprint

# Exceptions
from exceptions.ErrorHandler import ErrorHandler

# App - Configuration
environment = Environment.EnvironmentFunctions.get_environment()
app = Flask(__name__)
app.config.from_object(environment)

# Login Manager
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Registres of the blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(system_a_blueprint)
app.register_blueprint(system_b_blueprint)
app.register_blueprint(system_c_blueprint)

'''
# *********************** Warning ******************
# Use only on the promised execution
# Creates test users
# **************************************************

from database import init_db, db_session
from models.auth.User import User
@app.before_first_request
def create_user():
    init_db()
    user1 = User(email='user1@user.com',
                 password= bcrypt.generate_password_hash('senha'),
                 name='Usuario 1',
                 username='user1')
    user2 = User(email='user2@user.com',
                 password= bcrypt.generate_password_hash('senha2'),
                 name='Usuario 2',
                 username='user2')
    db_session.add_all([user1, user2])

    db_session.commit()
'''

# App - Default error setting
@app.errorhandler(ErrorHandler)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response, error.status_code

 # App - Start
if __name__ == "__main__":
    app.run()
