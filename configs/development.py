from configs.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/flask_catalog'
    JWT_SECRET = 'v3TkL5BD7nt9ANszKX4@u8qK$eGS'

