from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for Flask-WTF forms
db = SQLAlchemy(app)

# Import models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    cover_image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

@app.route("/")
def home():
    books = Book.query.all()
    return render_template("index.html", books=books)

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        cover_image = request.form["cover_image"]
        description = request.form["description"]

        # Add book to the database
        new_book = Book(title=title, author=author, cover_image=cover_image, description=description)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add_book.html")

if __name__ == "__main__":
    app.run(debug=True)
