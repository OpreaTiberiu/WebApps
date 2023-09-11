from flask import Flask, render_template, request
from post import Posts
from form import Form
from flask_bootstrap import Bootstrap5


posts = Posts()
app = Flask(__name__)
app.secret_key = "some secret string"
bootstrap = Bootstrap5(app)


def get_static_image(img_name):
    return f"../static/assets/img/{img_name}"


def get_contact_template_with_title(title):
    return render_template(
        "contact.html",
        title=title,
        subtitle="Have questions? I have answers.",
        header_image=get_static_image("contact-bg.jpg")
    )


def get_main_template(title, subtitle, image_url):
    return render_template(
        "index.html",
        title=title,
        subtitle=subtitle,
        header_image=image_url,
        posts=posts.data.values()
    )


@app.route('/login', methods=["POST", "GET"])
def login():
    form = Form()
    form.validate_on_submit()
    if request.method == 'POST':
        for key, val in request.form.items():
            print(key, val)
        if form.validate_on_submit():
            if form.email.data == "admin@email.com" and form.password.data == "12345678":
                return get_main_template(
                    title="Hello admin",
                    subtitle="You the bo$$",
                    image_url="https://media.tenor.com/Z6gmDPeM6dgAAAAC/dance-moves.gif"
                )
            else:
                return get_main_template(
                    title="Hello stranger",
                    subtitle="who are you?",
                    image_url="https://media.tenor.com/rB8hWIin-2IAAAAC/hmm-suspect.gif"
                )
    return render_template(
        "login.html",
        title="Login",
        form=form,
        header_image=get_static_image("home-bg.jpg")
    )


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "GET":
        return get_contact_template_with_title("Contact me")
    elif request.method == 'POST':
        for key, val in request.form.items():
            print(key, val)
            return get_contact_template_with_title("Message sent!")

    return home()


@app.route('/posts/<int:post_id>')
def get_post(post_id):
    print(posts.data[post_id]["image_url"])
    return render_template(
        "post.html",
        title=posts.data[post_id]["title"],
        subtitle=posts.data[post_id]["subtitle"],
        header_image=posts.data[post_id]["image_url"],
        post=posts.data[post_id])


@app.route('/about')
def about():
    return render_template(
        "about.html",
        title="About Me",
        subtitle="This is what I do.",
        header_image=get_static_image("about-bg.jpg")
    )


@app.route('/')
def home():
    return get_main_template(
        title="My Blog",
        subtitle="Simple blog using bootsrap.",
        image_url=get_static_image("home-bg.jpg")
    )


if __name__ == "__main__":
    app.run(debug=True)
