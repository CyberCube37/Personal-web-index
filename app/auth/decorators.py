from functools import wraps
from flask import abort, flash
from flask_login import current_user

def add(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if current_user.is_anonymous:
			return abort(401)
		if not current_user.add:
			return abort(403)
		return f(*args, **kwargs)
	return decorated_function

def remove(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if current_user.is_anonymous:
			return abort(401)
		if not current_user.remove:
			return abort(403)
		return f(*args, **kwargs)
	return decorated_function
