from configs.base import BaseConfig


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/flask_catalog'