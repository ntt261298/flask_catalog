from configs.base import BaseConfig


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/flask_catalog_test'
    JWT_SECRET = 'M67%RnPqTfuTarFGTKd4e$*w!tdj'
