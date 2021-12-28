import os
from flask import Flask
from config import Config, DevelopementConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_paranoid import Paranoid

import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
migrate = Migrate()
sess = Session()
paranoid = Paranoid()
paranoid.redirect_view = '/'

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app, db)
	sess.init_app(app)
	paranoid.init_app(app)

	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp)

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	if not app.debug and not app.testing:
  

		if app.config['LOG_TO_STDOUT']:
			stream_handler = logging.StreamHandler()
			stream_handler.setLevel(logging.INFO)
			app.logger.addHandler(stream_handler)
		else:
			if not os.path.exists('logs'):
				os.mkdir('logs')
			file_handler = RotatingFileHandler('logs/web_index.log',
											   maxBytes=10240, backupCount=10)
			file_handler.setFormatter(logging.Formatter(
				'%(asctime)s %(levelname)s: %(message)s '
				'[in %(pathname)s:%(lineno)d]'))
			file_handler.setLevel(logging.INFO)
			app.logger.addHandler(file_handler)

		app.logger.setLevel(logging.INFO)
		app.logger.info('Web_index startup')

	return app

from app import models

