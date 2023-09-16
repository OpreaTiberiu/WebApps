from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField


class Form(FlaskForm):
    title = StringField(label="Blog post Title", validators=[DataRequired()])
    subtitle = StringField(label="Blog post subtitle", validators=[DataRequired()])
    author = StringField(label="Your name", validators=[DataRequired()])
    img_url = StringField(label="Blog post Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField(label="Submit post")
