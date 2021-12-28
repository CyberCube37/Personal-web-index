from flask import render_template
from app import db
from app.errors import bp

@bp.app_errorhandler(404)
def page_not_found(e):
	#render 404.html when http response code is 404
	return render_template('404.html'), 404

@bp.app_errorhandler(405)
def method_not_allowed(e):
	#render 405.html when http response code is 405
	return render_template('405.html'), 405

@bp.app_errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500
	