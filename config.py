from datetime import timedelta


class Config(object):
    print("Config Start")
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    WTF_CSRF_ENABLED = False
    JWT_SECRET_KEY = ''
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=4)


class ProductionConfig(Config):
    JWT_SECRET_KEY = ''
    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(Config):
    DEBUG = True
    JWT_SECRET_KEY = 'PALAVRA_SECRETA_DESENVOLVIMENTO'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///developer.db'


class TestingConfig(Config):
    TESTING = True
