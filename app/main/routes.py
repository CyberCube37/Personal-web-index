from app import db
from app.main.forms import AddUrlForm, AddTagForm, EditUrlForm, EditTagForm
from app.auth.decorators import add, remove
from app.models import Tag, Link, User
from app.main import bp

from flask import render_template, flash, redirect, url_for, request, Markup
from flask_login import login_required, current_user

@bp.route('/', methods=['GET'])
def index():
	#get all tags from the database and render them as a list
	tags = Tag.query.order_by('name')
	return render_template('tags.html', tags=tags, title="Categories")


@bp.route('/get_tag/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
	#get all urls that have the tag with id tag_id and render them as a list
	tag = Tag.query.filter_by(id=tag_id).first()
	if tag:
		urls = Link.query.with_parent(tag).all()
		return render_template('urls.html', urls=urls, current=tag.id, title=tag.name.capitalize())
	else:
		flash("No such category exists!", "error")
		return redirect(url_for('main.index'))

@bp.route('/add_url', methods=['GET', 'POST'])
@add
def add_url():
	#you must be logged in to add a url

	#initiate the form with all tags from the database as choices for url tags
	form = AddUrlForm()
	form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by('name')]

	if form.validate_on_submit():
		#when form is submitted check if an entry with this url already exists in the database
		url = Link.query.filter_by(url=form.url.data).first()
		if url:
			flash(Markup("An entry with this URL already exists, see <a href='{}'>here</a>".format(url_for("main.get_tag",tag_id=url.tags[0].id, _anchor=url.id))), "warning")
			return render_template('add_url.html', form=form, title="Add URL") 
		tags = []
		if not form.new_tags.data and not form.tags.data:
			#if no tags are selected and no new tags are added automatically add this url to uncategorized
			uncat = Tag.query.filter_by(name="uncategorized").first()
			if not uncat:
				#if tag uncategorized doesn't exist yet create it first
				uncat = Tag(name="uncategorized")
				db.session.add(uncat)
			tags.append(uncat)
		else:
			if form.tags.data:
				#add every selected tag to the url
				for tag in form.tags.data:
					new_tag = Tag.query.filter_by(id=tag).first()
					tags.append(new_tag)

			if form.new_tags.data:
				#if user entered new tags, add the tags to the database if they do not already exist and then add them to the url
				for tag in form.new_tags.data.split(', '):
					new_tag = Tag.query.filter_by(name=tag.lower()).first()
					if not new_tag:
						new_tag = Tag(name=tag.lower())
						db.session.add(new_tag)
						tags.append(new_tag)
					elif new_tag not in tags:
						tags.append(new_tag)

		#create new url entity and add it to the database
		new_url = Link(title=form.title.data, url=form.url.data, description=form.description.data, tags=tags)
		db.session.add(new_url)
		db.session.commit()

		flash("Successfully added URL {}!".format(new_url.title), "success")
		return redirect(url_for('main.get_tag', tag_id=tags[0].id, _anchor=new_url.id))

	return render_template('add_url.html', form=form, title="Add URL")

@bp.route('/add_tag', methods=['GET', 'POST'])
@add
def add_tag():
	#you must be logged in to add a tag
	#initiate the form
	form = AddTagForm()

	if form.validate_on_submit():
		#when form is submitted check if the tag already exists, if not add it to the database
		tmp = Tag.query.filter_by(name=form.name.data.lower()).first()
		if not tmp:
			new_tag = Tag(name=form.name.data.lower())
			db.session.add(new_tag)
			db.session.commit()

			flash("Successfully added category {}!".format(new_tag.name), "success")
			return redirect(url_for('main.index', _anchor=new_tag.id))
		else:
			flash(Markup("That category already exists, see <a href='{}'>here</a>!".format(url_for("main.index", _anchor=tmp.id))), "warning")
		
	return render_template('add_tag.html', form=form, title="Add category")

@bp.route('/edit_url/<int:url_id>', methods=['GET', 'POST'])
@remove
def edit_url(url_id):
	#you must be logged in to edit a url
	#get the url entry from the database and prepopulate the form with it's data
	url = Link.query.filter_by(id=url_id).first()
	form = EditUrlForm(obj=url)
	#tag choices are all tags from the database
	form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by('name')]
	if request.method == 'GET':
		#if request method is GET prepopulate the selected tags with the tags in the url entry
		form.tags.data = [t.id for t in url.tags]

	if form.validate_on_submit():
		#when form is submitted
		tmp = []
		if not form.tags.data and not form.new_tags.data:
			#if no tags are selected and no new tags are added automatically add this url to uncategorized
			if not Tag.query.filter_by(name="uncategorized").first():
				#if tag uncategorized doesn't exist yet create it first
				new_tag = Tag(name="uncategorized")
				db.session.add(new_tag)
				tmp.append(new_tag)
			else:
				tmp.append(Tag.query.filter_by(name="uncategorized").first())
		else:
			if form.tags.data:
				#update the url's tags with the selected ones 
				tmp = [Tag.query.filter_by(id=t).first()for t in form.tags.data]
			if form.new_tags.data:
				#if user entered new tags, add the tags to the database, if they do not already exist, and then add them to the url
				for tag in form.new_tags.data.split(', '):
					new_tag = Tag.query.filter_by(name=tag.lower()).first()
					if not new_tag:
						new_tag = Tag(name=tag.lower())
						db.session.add(new_tag)
						tmp.append(new_tag)
					elif new_tag not in tmp:
						tmp.append(new_tag)

		form.tags.data = tmp
		#update the url entry with the entered data
		form.populate_obj(url)
		url.id = url_id

		db.session.commit()

		flash("Successfully updated URL {}!".format(url.title), "success")
		return redirect(url_for('main.get_tag', tag_id=url.tags[0].id, _anchor=url.id))
		
	return render_template('edit_url.html', form=form, title="Edit URL")

@bp.route('/edit_tag/<int:tag_id>', methods=['GET', 'POST'])
@remove
def edit_tag(tag_id):
	#you must be logged in to edit a url
	#get the tag from the database and prepopulate the form with it's data
	tag = Tag.query.filter_by(id=tag_id).first()
	form = EditTagForm(obj=tag)

	if form.validate_on_submit():
		#when form is submitted update the tag's data with the entered data
		form.name.data = form.name.data.lower()
		form.populate_obj(tag)
		tag.id = tag_id
		db.session.commit()
		flash("Successfully updated category {}!".format(tag.name), "success")
		return redirect(url_for('main.index', _anchor=tag.id))
		
	return render_template('edit_tag.html', form=form, title="Edit category")



@bp.route('/delete_tag/<int:tag_id>', methods=['GET'])
@remove
def delete_tag(tag_id):
	#you must be logged in to delete a tag
	#check if the tag exists, if it exists delete it and redirect to the home page
	tag = Tag.query.filter_by(id=tag_id).first()
	if not tag:
		flash("No such category exists!", "error")
	if tag.name == "uncategorized":
		flash("Can't delete category uncategorized", "error")
	else:
		flash("Successfully deleted category {}!".format(tag.name), "success")
		db.session.delete(tag)
		db.session.commit()
	return redirect(url_for('main.index'))

@bp.route('/delete_url/<int:url_id>', methods=['GET'])
@remove
def delete_url(url_id):
	#you must be logged in to delete a url
	#check if the url exists, if it exists delete it and redirect to the previous page or the home page
	if request.args.get("next"):
		next_site = url_for("main.get_tag", tag_id=int(request.args["next"]))
	else:
		next_site = url_for("main.index")
	link = Link.query.filter_by(id=url_id).first()
	if not link:
		flash("No such URL exists!", "error")
	else:
		flash("Successfully deleted URL {}!".format(link.title), "success")
		db.session.delete(link)
		db.session.commit()
	return redirect(next_site)