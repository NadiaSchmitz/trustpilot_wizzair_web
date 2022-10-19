from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tpw.db'
app.config["SQLALCHEMY_TRACK_MODIFIKATIONS"] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(600), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

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


@app.route('/articles')
def articles():
    return render_template('articles.html')


@app.route('/create_article', methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "Ein Fehler ist aufgetreten"
    else:
        return render_template("create_article.html")

if __name__ == "__main__":
    app.run(debug=True)
