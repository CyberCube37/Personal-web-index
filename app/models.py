from app import db

tag_link = db.Table('tag_link',
	db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'), primary_key=True),
	db.Column('link_id', db.Integer,db.ForeignKey('link.id'),primary_key=True)
)

class Link(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(50),nullable=False)
	url = db.Column(db.Text,nullable=False)
	description = db.Column(db.Text,nullable=False)
	tags = db.relationship('Tag',secondary=tag_link,backref=db.backref('links_associated',lazy=True))

class Tag(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(20), nullable=False)
