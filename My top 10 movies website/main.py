from database_manager import *
from movie_form import Small_Form, Form
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from movie_api_manager import get_movies_by_title
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/delete/<int:movie_id>')
def delete(movie_id):
    # book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/edit/<int:movie_id>', methods=["POST", "GET"])
def edit(movie_id):
    movie_to_edit = db.get_or_404(Movie, movie_id)
    form = Form(
        title=movie_to_edit.title,
        rating=movie_to_edit.rating,
        year=movie_to_edit.year,
        description=movie_to_edit.description,
        ranking=movie_to_edit.ranking,
        review=movie_to_edit.review,
        img_url=movie_to_edit.img_url,
    )

    if request.method == 'POST':
        if form.validate_on_submit():
            movie_to_edit.title = form.title.data
            movie_to_edit.rating = form.rating.data
            movie_to_edit.year = form.year.data
            movie_to_edit.description = form.description.data
            movie_to_edit.ranking = form.ranking.data
            movie_to_edit.review = form.review.data
            movie_to_edit.img_url = form.img_url.data
            db.session.commit()
            return redirect(url_for('home'))
    return render_template(
        "movie.html",
        title=movie_to_edit.title,
        page_title=f"Edit {movie_to_edit.title}",
        form=form
    )


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    form = Form(
        title=request.args.get("movie_title"),
        year=request.args.get("movie_year"),
        description=request.args.get("movie_desc"),
        img_url=request.args.get("movie_img"),
    )
    if request.method == 'POST':
        if form.validate_on_submit():
            add_record(
                current_app=app,
                title=form.title.data,
                rating=form.rating.data,
                year=form.year.data,
                description=form.description.data,
                ranking=form.ranking.data,
                review=form.review.data,
                img_url=form.img_url.data,
            )
            return redirect(url_for('home'))
    return render_template(
        "movie.html",
        title="Add a movie",
        page_title="Add a new movie",
        form=form
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    form = Small_Form()
    if request.method == 'POST':
        if form.validate_on_submit():
            movies = get_movies_by_title(form.title.data)
            return render_template(
                "select.html",
                title="Add a movie",
                page_title="Add a new movie",
                form=form,
                movies=movies
            )
    return render_template(
        "add.html",
        title="Add a movie",
        page_title="Add a new movie",
        form=form
    )


global_variable_for_testing_delete = False


@app.route('/')
def home():
    global global_variable_for_testing_delete
    if not global_variable_for_testing_delete:
        global_variable_for_testing_delete = True
        if not get_record_by_title(app, "Phone Booth"):
            add_record(app)
        if not get_record_by_title(app, "Avatar The Way of Water"):
            add_record(
                app,
                title="Avatar The Way of Water",
                year=2022,
                description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
                rating=7.3,
                ranking=9,
                review="I liked the water.",
                img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
            )
    return render_template("index.html", movies=get_records(app))


if __name__ == '__main__':
    app.run(debug=True)
