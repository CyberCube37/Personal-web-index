from flask import render_template, flash, redirect, url_for, session, request, current_app
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app.auth.forms import LoginForm
from app.auth import bp
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		flash("You are already logged in!", "warning")
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("Wrong username or password, please try again!", "error")
			return redirect(url_for('auth.login'))
		login_user(user, remember=form.remember_me.data)
		flash('Successfully logged in!', "success")
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('main.index')
		return redirect(next_page)
	return render_template('auth/login.html', title=('Sign In'), form=form)


@bp.route('/logout')
def logout():
	logout_user()
	next_page = request.args.get('next')
	if not next_page or url_parse(next_page).netloc != '':
		next_page = url_for('main.index')
	if not current_user.is_anonymous:
		flash("You have Successfully logged out!", "success")
	return redirect(next_page)