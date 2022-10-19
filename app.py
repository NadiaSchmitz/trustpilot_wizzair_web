from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tpw.db'
app.config["SQLALCHEMY_TRACK_MODIFIKATIONS"] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about_me')
def about_me():
    return render_template('about_me.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/posts')
def posts():
    posts = Post.query.order_by(Post.date).all()
    return render_template('posts.html', posts=posts)


@app.route('/create_post', methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        link = request.form["link"]

        post = Post(title=title, text=text, link=link)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return "Ein Fehler ist aufgetreten"
    else:
        return render_template("create_post.html")

if __name__ == "__main__":
    app.run(debug=True)
