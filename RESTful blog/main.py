from post_form import Form
from database_manager import *
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from datetime import datetime
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=get_records(app))


@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = get_record_by_id(app, post_id)
    return render_template("post.html", post=requested_post)


@app.route('/new_post', methods=["GET", "POST"])
def new_post():
    form = Form()
    if request.method == "POST" and form.validate_on_submit():
        add_record(
            current_app=app,
            title=form.title.data,
            date=datetime.now().strftime("%b %d, %Y"),
            subtitle=form.subtitle.data,
            body=form.body.data,
            author=form.author.data,
            img_url=form.img_url.data
        )
        return render_template("index.html", all_posts=get_records(app))

    return render_template("make-post.html", form=form)


@app.route('/edit_post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    requested_post = get_record_by_id(app, post_id)
    form = Form(
        title=requested_post.title,
        subtitle=requested_post.subtitle,
        body=requested_post.body,
        author=requested_post.author,
        img_url=requested_post.img_url
    )
    if request.method == "POST" and form.validate_on_submit():
        print(form.author.data)
        update_record(
            current_app=app,
            post_id=post_id,
            title=form.title.data,
            date=datetime.now().strftime("%b %d, %Y"),
            subtitle=form.subtitle.data,
            body=form.body.data,
            author=form.author.data,
            img_url=form.img_url.data
        )
        return render_template("index.html", all_posts=get_records(app))

    return render_template("make-post.html", form=form)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    delete_record(app, post_id)
    return redirect(url_for('get_all_posts'))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
