import re
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Regexp, Optional, ValidationError
from wtforms.fields.html5 import URLField, DateField, IntegerField, URLField


class BaseBookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[
                       DataRequired(), Regexp(r"^([A-Z]+:)?\d*$")])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    date = DateField("Publication date",
                     format='%Y-%m-%d', validators=[Optional()])
    pages = IntegerField("Pages number", validators=[Optional()])
    url = URLField("frontPage", render_kw={
        "placeholder": "http://www.example.com"})
    language = StringField("Language", render_kw={
        "placeholder": "un"})

    def validate_url(form, field):
        if form.url.data:
            if not re.match(
                    "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$", field.data):
                raise ValidationError('Invalid URL.')


class ImportForm(FlaskForm):
    books = FieldList(FormField(BaseBookForm))
    remove = SubmitField("REMOVE_LAST")
    submit = SubmitField("IMPORT")


class BookForm(BaseBookForm):
    submit = SubmitField("ADD/CHANGE")


class BaseSearchForm(FlaskForm):
    search = StringField("Search")
    title = StringField("Title")
    author = StringField("Author")
    publisher = StringField("Publisher")
    subject = StringField("Subject")
    isbn = StringField("ISBN", validators=[Regexp(r"^([A-Z]+:)?\d*$")])


class SearchForm(BaseSearchForm):
    submit = SubmitField("IMPORT")


class BaseFilterForm(FlaskForm):
    title = StringField("Title")
    author = StringField("Author")
    language = StringField("language")
    startdate_field = DateField(
        "Date from", format='%Y-%m-%d')
    enddate_field = DateField(
        "Date To", format='%Y-%m-%d')

    def validate_enddate_field(form, field):
        if form.startdate_field.data and form.enddate_field.data:
            if field.data < form.startdate_field.data:
                raise ValidationError(
                    "End date must not be earlier than start date.")


class FilterForm(BaseFilterForm):
    startdate_field = DateField(
        "Date from", format='%Y-%m-%d', validators=[Optional()])
    enddate_field = DateField(
        "Date To", format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField("FILTER")
