from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

# App Config
app = Flask(__name__, )
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


# Celery
from app.celery import make_celery
celery = make_celery(app)

# Database
from config import secret
app.secret_key = secret
migrate = Migrate(app, db)


# Controllers
from app.user.controller import bp as user_bp
app.register_blueprint(user_bp)
from app.profile.controller import bp as profile_bp
app.register_blueprint(profile_bp)
from app.wallet.controller import bp as wallet_bp
app.register_blueprint(wallet_bp)
from app.transaction.controller import bp as transaction_bp
app.register_blueprint(transaction_bp)
from app.airtime.controller import bp as airtime_bp
app.register_blueprint(airtime_bp)

# Error handlers
from .error_handlers import *