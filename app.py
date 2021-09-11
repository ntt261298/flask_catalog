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

from models.user import User
from models.admin import Admin
from models.category import Category
from models.item import Item

