import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import app_config

app = Flask(__name__)

if os.environ.get('ENV') in ['local', 'development', 'production']:
    app.config.from_object(app_config[os.environ['ENV']])
else:
    app.config.from_object(app_config['local'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models.user
import models.admin
import models.category
import models.item
import errors
import controllers.user
