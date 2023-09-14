from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Maps (as URL)', validators=[DataRequired(), URL()])
    open = StringField('Opening Time e.g. 8 A.M.', validators=[DataRequired()])
    close = StringField('Closing Time e.g. 10 P.M.', validators=[DataRequired()])
    coffee_rating = SelectField(
        label='Coffee rating',
        validators=[DataRequired()],
        choices=["☕" * i for i in range(1, 6)]
    )
    wifi_rating = SelectField(
        label='Wifi rating',
        validators=[DataRequired()],
        choices=["✘"] + ["💪" * i for i in range(1, 6)]
    )
    power_rating = SelectField(
        label='Power socket rating',
        validators=[DataRequired()],
        choices=["✘"] + ["🔌" * i for i in range(1, 6)]
    )
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            with open('cafe-data.csv', mode="a", newline='', encoding='utf-8') as csv_file:
                csv_file.write(
                    f"\n{form.cafe.data},{form.location.data},{form.open.data},{form.close.data}," + \
                    f"{form.coffee_rating.data},{form.wifi_rating.data},{form.power_rating.data}"
                )
            return render_template("index.html")

    return render_template('book.html', form=form)


@app.route('/cafes')
def cafes():
    with open("t.txt", "w") as f:
        f.write("ASDFads")
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
