from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField, DateField
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, url, ValidationError


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


class FilterForm(FlaskForm):
    title = StringField("Title")
    author = StringField("Author")
    language = StringField("language")
    date_from = DateField("Date from", format='%Y-%m-%d')
    date_to = DateField("Date To", format='%Y-%m-%d')
    submit = SubmitField("FILTER")

    def validate_date_to(form, field):
        if field.data < form.date_from.data:
            raise ValidationError(
                "End date must not be earlier than start date.")
