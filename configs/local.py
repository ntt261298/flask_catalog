from configs.base import BaseConfig


class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/flask_catalog'
    JWT_SECRET = '&!!xs^r@rhHvKmP&CuUfHa74EkUB'
