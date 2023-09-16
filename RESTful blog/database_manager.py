from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_record_by_id(current_app, id):
    with current_app.app_context():
        return db.session.execute(db.select(BlogPost).filter(BlogPost.id == id)).scalar()


def get_records(current_app):
    with current_app.app_context():
        result = db.session.execute(db.select(BlogPost).order_by(BlogPost.date))
        return result.scalars().all()


def update_record(
        current_app,
        post_id,
        title,
        date,
        subtitle,
        body,
        author,
        img_url
):
    with current_app.app_context():
        record = db.get_or_404(BlogPost, post_id)
        record.title = title
        record.subtitle = date
        record.img_url = subtitle
        record.author = author
        record.body = body
        record.img_url = img_url
        db.session.commit()

def add_record(
        current_app,
        title,
        date,
        subtitle,
        body,
        author,
        img_url
):
    with current_app.app_context():
        new_data = BlogPost(
            title=title,
            subtitle=subtitle,
            date=date,
            body=body,
            author=author,
            img_url=img_url
        )
        db.session.add(new_data)
        db.session.commit()

def delete_record(current_app, post_id):
    with current_app.app_context():
        post_to_delete = db.get_or_404(BlogPost, post_id)
        db.session.delete(post_to_delete)
        db.session.commit()


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
