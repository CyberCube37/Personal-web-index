from app import db, login
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

tag_link = db.Table('tag_link',
	db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'), primary_key=True),
	db.Column('link_id', db.Integer,db.ForeignKey('link.id'),primary_key=True)
)

class Link(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.Text,nullable=False)
	url = db.Column(db.Text,nullable=False)
	description = db.Column(db.Text,nullable=False)
	tags = db.relationship('Tag',secondary=tag_link,backref=db.backref('links_associated',lazy=True))

	def __repr__(self):
		return '<Link {}>'.format(self.title)

class Tag(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return '<Tag {}>'.format(self.name)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	add = db.Column(db.Boolean, default=False)
	remove = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class MyAnonymousUser(AnonymousUserMixin):
	add = False
	remove = False

	
