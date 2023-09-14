from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

db = SQLAlchemy()
db.init_app(app)


class Form(FlaskForm):
    name = StringField(label="Book Name", validators=[DataRequired()])
    author = StringField(label="Book author", validators=[DataRequired()])
    rating = IntegerField(label="Book rating out of a maximum of 10",
                          validators=[DataRequired(), NumberRange(min=0, max=10,
                                                                  message="Must be a number between 0 and 10")])
    submit = SubmitField(label="Add")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()


def add_record(current_app, title="Harry Potter", author="J. K. Rowling", rating=9.3):
    with current_app.app_context():
        new_book = Book(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()


def get_records(current_app):
    with current_app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        return result.scalars().all()


@app.route('/')
def home():
    if len(get_records(app)) < 1:
        add_record(app)
    return render_template("index.html", books=get_records(app))


@app.route('/delete/<int:id>')
def delete(id):
    # book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/edit/<int:id>', methods=["POST", "GET"])
def edit(id):
    book_to_edit = db.get_or_404(Book, id)
    form = Form(
        name=book_to_edit.title,
        author=book_to_edit.author,
        rating=book_to_edit.rating
    )

    if request.method == 'POST':
        if form.validate_on_submit():
            book_to_edit.author = form.author.data
            book_to_edit.title = form.name.data
            book_to_edit.rating = form.rating.data
            db.session.commit()
            return redirect(url_for('home'))
    return render_template(
        "book.html",
        title=book_to_edit.title,
        page_title=f"Edit {book_to_edit}",
        form=form
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    form = Form()
    if request.method == 'POST':
        if form.validate_on_submit():
            add_record(
                current_app=app,
                title=form.name.data,
                author=form.author.data,
                rating=form.rating.data
            )
            return redirect(url_for('home'))
    return render_template(
        "book.html",
        title="Add a book",
        page_title="Add a new book",
        form=form
    )


if __name__ == "__main__":
    app.run(debug=True)
