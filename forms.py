from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, url


class BookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    pubDate = DateField("Publication date", format='%Y-%m-%d')
    pages = IntegerField("Pages number")
    fronPage = URLField("frontPage", validators=[url()])
    language = TextField("Language")
    submit = SubmitField("ADD/CHANGE")


class SearchForm(FlaskForm):
    search = StringField("Search")
    title = StringField("Title")
    author = StringField("Author")
    publisher = StringField("Publisher")
    subject = StringField("Subject")
    isbn = StringField("ISBN")
    submit = SubmitField("IMPORT")
