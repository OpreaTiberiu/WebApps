from flask import Flask, render_template
from post import Posts


posts = Posts()
app = Flask(__name__)


@app.route('/posts/<int:post_id>')
def get_post(post_id):
    return render_template("post.html", post=posts.data[post_id])


@app.route('/')
def home():
    return render_template("index.html", posts=posts.data.values())


if __name__ == "__main__":
    app.run(debug=True)
