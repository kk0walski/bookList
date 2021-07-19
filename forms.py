from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, url, ValidationError
from wtforms.fields.html5 import URLField, DateField


class BookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    pubDate = DateField("Publication date", format='%Y-%m-%d')
    pages = IntegerField("Pages number")
    fronPage = URLField("frontPage", validators=[url()])
    language = StringField("Language")
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
    startdate_field = DateField("Date from", format='%Y-%m-%d')
    enddate_field = DateField("Date To", format='%Y-%m-%d')
    submit = SubmitField("FILTER")

    def validate_enddate_field(form, field):
        if form.startdate_field.data and form.enddate_field.data:
            if field.data < form.startdate_field.data:
                raise ValidationError(
                    "End date must not be earlier than start date.")
