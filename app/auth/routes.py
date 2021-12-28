from flask import render_template, flash, redirect, url_for, session, request, current_app
from werkzeug.security import check_password_hash
from app.auth.forms import LoginForm
from app.auth.decorators import login_required
from app.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
	if session.get('active'):
		#if user is already logged in redirect him to first page
		flash("You are already logged in!", "warning")
		return redirect(url_for("main.index"))

	#code to redirect the user to the previous page after logging in
	if request.args.get("next"):
		next_site = request.args["next"]
	else:
		next_site = "main.index"

	#initiate the login form
	form = LoginForm(redirect=next_site)

	if form.validate_on_submit():
		#when form is submitted check if password and username match
		if form.username.data == current_app.config["USERNAME"] and  check_password_hash(current_app.config["PASSWORD"], form.password.data):
			session["active"] = True
			flash('Successfully logged in!', "success")
			print(form.redirect.data)
			return redirect(form.redirect.data)
		else:
			flash("Wrong username or password, please try again!", "error")

	return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout', methods=['GET'])
@login_required
def logout():
	#if the user is logged in log him out and redirect to the previous page
	if request.args.get("next"):
		next_site = request.args["next"]
	else:
		next_site = "main.index"
	session.pop('active')
	flash("You have Successfully logged out!", "success")
	return redirect(next_site)