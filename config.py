import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = '910386943@qq.com'
    FLASKY_ADMIN = '910386943@qq.com'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
#   FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
#   MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#   MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USERNAME = '910386943@qq.com'
    MAIL_PASSWORD = 'flqeqfyvhsegbbba'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/dev_flask'

config = {
'development':DevelopmentConfig,
'default':DevelopmentConfig

}
