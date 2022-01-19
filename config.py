import os
from redis import from_url
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	USERNAME = os.environ.get('USERNAME') or 'admin'
	PASSWORD = os.environ.get('PASSWORD') or 'pbkdf2:sha256:260000$WuZqakhSe5xf4JuD$70f829424a9ac9c05004d6b5515d12acf4bc35ba5cc016c7b280521d8df1a154'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SESSION_COOKIE_SECURE = True
	SESSION_COOKIE_HTTPONLY = True
	SESSION_TYPE = "redis"
	SESSION_PERMANENT = False
	SESSION_USE_SIGNER = True
	REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
	SESSION_REDIS = from_url(REDIS_URL)
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

class DevelopementConfig(Config):
	SESSION_COOKIE_SECURE = False
	TESTING = True
	SESSION_TYPE = "filesystem"