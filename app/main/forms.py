from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TextAreaField, SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.validators import InputRequired, URL

class AddUrlForm(FlaskForm):
	title = StringField('Title', validators=[InputRequired(message="Title cannot be empty!")])
	url = URLField('Url', validators=[InputRequired(message="URL cannot be empty!"), URL(message="Please enter a valid URL!")])
	description = TextAreaField('Description')
	tags = SelectMultipleField('Tags', coerce=int, option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
	new_tags = StringField('Add tags')
	submit = SubmitField('Add URL')

class EditUrlForm(FlaskForm):
	title = StringField('Title', validators=[InputRequired(message="Title cannot be empty!")])
	url = URLField('Url', validators=[InputRequired(message="URL cannot be empty!"), URL(message="Please enter a valid URL!")])
	description = TextAreaField('Description')
	tags = SelectMultipleField('Tags', coerce=int, option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
	new_tags = StringField('Add tags')
	submit = SubmitField('Update URL')

class AddTagForm(FlaskForm):
	name = StringField('Name', validators=[InputRequired(message="Name cannot be empty!")])
	submit = SubmitField('Add tag')

class EditTagForm(FlaskForm):
	name = StringField('Name', validators=[InputRequired(message="Name cannot be empty!")])
	submit = SubmitField('Update tag')
