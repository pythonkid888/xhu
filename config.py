#-*- coding:utf-8 -*-

import os

base = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'i love you'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[x乎]'
    FLASKY_MAIL_SENDER = 'DZ<496487991@qq.com>'
    FLASKY_ADMIN = '496487991@qq.com'
    FLASKY_PER_PAGE = 20
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 496487991
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base, 'dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base, 'test.sqlite')


class ProductionConfig(Config):
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(base, 'data.sqlite')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        #把错误发送到管理员邮箱
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_SSL', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost = (cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr = cls.FLASKY_MAIL_SENDER,
            toaddrs = [cls.FLASKY_ADMIN],
            subject = cls.FLASKY_MAIL_SUBJECT_PREFIX + 'Application Error',
            credentials = credentials,
            secure = secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        
class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        
        #输出到stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig
}
