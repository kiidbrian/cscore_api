import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'h@ck5t0ck070619881n3tNf@2el3w'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://postgres:password@localhost/hackathon_db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig,
    'SUCCESS': "00",
    'FAILURE': "01",
    'ERROR': "02",
    'SMS_PROVIDER': "http://itxt.ikernelnetworks.com/bulksms.php",
    'SMS_API_KEY': "rinBKXH9dNL4IEMYvkl73FgJoz0Z2yDP",
    'MOMO_PROVIDER': "http://ec2-52-89-184-99.us-west-2.compute.amazonaws.com/api/v1/payment",
    'MOMO_API_KEY': "9217fd994e104fb147c615554d22141a115330d469ba11535952516559362210"
}
