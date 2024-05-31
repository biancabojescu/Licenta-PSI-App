from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, routes, routes_autentificare, routes_dashboard

with app.app_context():
    db.create_all()
    models.create_pacienti_tables()
