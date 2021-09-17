from configs.local import LocalConfig
from configs.development import DevelopmentConfig
from configs.production import ProductionConfig
from configs.test import TestConfig

app_config = {
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
}
