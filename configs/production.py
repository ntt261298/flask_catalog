from configs.base import BaseConfig


# Those configs should be stored in a private place
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/flask_catalog'
    JWT_SECRET = 'gx#Eq6fxDQpBoaoS8fW9#&VwWSV!'
