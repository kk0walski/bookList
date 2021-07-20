from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Regexp, Optional, URL
from wtforms.fields.html5 import URLField, DateField, IntegerField, URLField


class BookForm(FlaskForm):
    isbn = StringField('ISBN', validators=[
                       DataRequired(), Regexp(r"^([A-Z]+:)?\d*$")])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    pubDate = DateField("Publication date",
                        format='%Y-%m-%d', validators=[Optional()])
    pages = IntegerField("Pages number", validators=[Optional()])
    url = URLField("frontPage", validators=[URL(), Optional()], render_kw={
        "placeholder": "http://www.example.com"})
    language = StringField("Language", render_kw={
        "placeholder": "un"})


class ImportForm(FlaskForm):
    books = FieldList(FormField(BookForm))
    remove = SubmitField("REMOVE")
    submit = SubmitField("IMPORT")


class BookFormSubmit(FlaskForm):
    isbn = StringField('ISBN', validators=[
                       DataRequired(), Regexp(r"^([A-Z]+:)?\d*$")])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    pubDate = DateField("Publication date",
                        format='%Y-%m-%d', validators=[Optional()])
    pages = IntegerField("Pages number", validators=[Optional()])
    url = URLField("frontPage", validators=[URL(), Optional()], render_kw={
        "placeholder": "http://www.example.com"})
    language = StringField("Language", render_kw={
        "placeholder": "un"})
    submit = SubmitField("ADD/CHANGE")


class SearchForm(FlaskForm):
    search = StringField("Search")
    title = StringField("Title")
    author = StringField("Author")
    publisher = StringField("Publisher")
    subject = StringField("Subject")
    isbn = StringField("ISBN", validators=[Regexp(r"^([A-Z]+:)?\d*$")])
    submit = SubmitField("IMPORT")


class FilterForm(FlaskForm):
    title = StringField("Title")
    author = StringField("Author")
    language = StringField("language")
    startdate_field = DateField(
        "Date from", format='%Y-%m-%d', validators=[Optional()])
    enddate_field = DateField(
        "Date To", format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField("FILTER")

    def validate_enddate_field(form, field):
        if form.startdate_field.data and form.enddate_field.data:
            if field.data < form.startdate_field.data:
                raise ValidationError(
                    "End date must not be earlier than start date.")
