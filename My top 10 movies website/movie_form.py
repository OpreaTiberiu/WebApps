from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange, URL


class Form(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    rating = FloatField(label="Movie Rating", validators=[
        DataRequired(),
        NumberRange(min=0, max=10, message="Must be between between 0 and 10")
    ])
    year = IntegerField(label="Movie Release Year", validators=[DataRequired()])
    description = StringField(label="Movie Description", validators=[DataRequired()])
    ranking = IntegerField(label="Movie Ranking", validators=[DataRequired()])
    review = StringField(label="Movie Review", validators=[DataRequired()])
    img_url = StringField(label="Movie Image URL", validators=[DataRequired(), URL()])

    submit = SubmitField(label="Add")


class Small_Form(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])

    submit = SubmitField(label="Search")