import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///readingtracker.db")


@app.route("/")
@login_required
def index():
    # gets the 5 most recent books that others on the website have logged so that they can be suggested books to the user
    suggestions = db.execute("SELECT title, author, genre FROM books WHERE not id = :id ORDER BY bookid DESC LIMIT 5",
                             id=session["user_id"])
    return render_template("homepage.html", suggestions=suggestions)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # gets the username and checks to make sure it is available and valid
    username = request.args.get("name").strip().lower()
    if len(username) >= 1 and not db.execute("SELECT * FROM users WHERE username = :username", username=username):
        return jsonify(True)
    return jsonify(False)


@app.route("/getInfo", methods=["GET"])
def getInfo():
    # sets up a list to hold all the information
    data = []

    # gets the current date
    today = datetime.date.today()

    # gets how many pages have been read by the user on each day this last week
    for num in range(7):
        diff = datetime.timedelta(days=6-num)
        day = today - diff
        pages = db.execute("SELECT SUM(pagesRead) FROM reading WHERE :id = id and readingDate = :date",
                           id=session["user_id"], date=day)
        pages = pages[0]["SUM(pagesRead)"]
        if pages == None:
            pages = 0
        data.append({"date": str(day), "pages": pages})

    # returns a list of dictionaries with the date and pages for each day this last week
    return jsonify(data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username").strip().lower())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # gets the username and makes sure something was inputted
        username = request.form.get("username").strip().lower()
        if not username:
            return apology("Missing username!")

        # makes sure the user entered password and confirmed it
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation or not password == confirmation:
            return apology("Make sure to include a password and confirm that same password!")

        # hashes the password and puts the user in the database
        hashPass = generate_password_hash(password)
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashPass)",
                            username=username, hashPass=hashPass)

        # lets the user know if the username is already taken
        if not result:
            return apology("Username is taken")

        # logs user in
        session["user_id"] = result

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/books")
@login_required
def books():
    # gets all the books that the user has logged
    books = db.execute("SELECT * FROM books WHERE id = :id", id=session["user_id"])
    return render_template("books.html", books=books)


@app.route("/addBook", methods=["GET", "POST"])
@login_required
def addBook():
    if request.method == "POST":
        # gets all the information that the user inputted
        title = request.form.get("title").strip()
        author = request.form.get("author").strip()
        genre = request.form.get("genre")
        startdate = request.form.get("startdate")
        finishdate = request.form.get("finishdate")

        # makes sure the user didn't leave anything blank (except the finishdate which can be left blank)
        if not title or not author or not genre or not startdate:
            return apology("Please enter all of the required information")

        # makes sure the finishdate is on or after the startdate
        if finishdate:
            if startdate > finishdate:
                return apology("Please enter a finishdate on or after the startdate")

        # makes sure the title of the book is unique
        if db.execute("SELECT * FROM books WHERE id = :id and title = :title", id=session["user_id"], title=title):
            return apology("Please enter a book title that you haven't already read")

        # inserts the book info into the database
        result = db.execute("INSERT INTO books (id, title, author, genre, startdate, finishdate) VALUES (:id, :title, :author, :genre, :startdate, :finishdate)",
                            id=session["user_id"], title=title, author=author, genre=genre, startdate=startdate, finishdate=finishdate)

        return redirect("/books")
    else:
        return render_template("addBook.html")


@app.route("/finishBook", methods=["GET", "POST"])
@login_required
def finishBook():
    if request.method == "POST":
        # gets the finishdate and title of the book
        finishdate = request.form.get("finish")
        title = request.form.get("unfinished")

        # makes sure nothing was left blank
        if not title or not finishdate:
            return apology("You must provide all the information")

        # gets the startdate of the book
        start = db.execute("SELECT startdate FROM books WHERE id = :id and title = :title", id=session["user_id"], title=title)
        start = start[0]["startdate"]

        # makes sure the finishdate was on or after the start date and if it is then updates the database
        if finishdate >= start:
            result = db.execute("UPDATE books SET finishdate = :finishdate WHERE id =:id and title = :title",
                                finishdate=finishdate, id=session["user_id"], title=title)
        else:
            return apology("The finishdate must be on or after the startdate")

        return redirect("/books")
    else:
        # gets all the books without a finishdate so that the user can pick from them
        notFinished = db.execute("SELECT title FROM books WHERE id = :id and finishdate = :finishdate",
                                 id=session["user_id"], finishdate="")
        return render_template("finishBook.html", notFinished=notFinished)


@app.route("/readingHistory", methods=["GET", "POST"])
@login_required
def readingHistory():
    # gets all the books that the user has logged
    books = db.execute("SELECT title FROM books WHERE id = :id", id=session["user_id"])
    if request.method == "POST":
        # gets the book that the user wants to see a history of and makes sure it wasn't blank
        bookHistoryRequested = request.form.get("bookHistoryRequested")
        if not bookHistoryRequested:
            return apology("You must select a book to see its reading history")

        # gets the reading logs for whatever book the person wanted to see a history of
        if bookHistoryRequested == "allBooks":
            logs = db.execute("SELECT * FROM reading WHERE id = :id", id=session["user_id"])
        else:
            logs = db.execute("SELECT * FROM reading WHERE id = :id and title = :title",
                              id=session["user_id"], title=bookHistoryRequested)

        return render_template("readingHistory.html", books=books, logs=logs)
    else:
        # originally it gets all the reading logs for that user
        logs = db.execute("SELECT * FROM reading WHERE id = :id", id=session["user_id"])
        return render_template("readingHistory.html", books=books, logs=logs)


@app.route("/logReading", methods=["GET", "POST"])
@login_required
def logReading():
    if request.method == "POST":
        # gets the info that the person inputted and makes sure it's not blank and that the pages are at least 1
        book = request.form.get("book")
        pagesRead = request.form.get("pages")
        readingDate = request.form.get("readingDate")
        if not book or not pagesRead or not readingDate or int(pagesRead) < 1:
            return apology("You must enter all of the information properly")

        # gets the startdate and finishdate for the book
        bookInfo = db.execute("SELECT startdate, finishdate FROM books WHERE id = :id and title = :title",
                              id=session["user_id"], title=book)
        start = bookInfo[0]["startdate"]
        finish = bookInfo[0]["finishdate"]

        # makes sure that the date the person read was on or after the startdate and on or before the finishdate
        if not finish == "":
            if readingDate < start or readingDate > finish:
                return apology("You must enter a reading date that is between the startdate and finishdate (inclusive)")
        else:
            if readingDate < start:
                return apology("You must enter a reading date that is on or after the startdate")

        # puts the reading info into the database
        result = db.execute("INSERT INTO reading (id, title, pagesRead, readingDate) VALUES (:id, :title, :pagesRead, :readingDate)",
                            id=session["user_id"], title=book, pagesRead=pagesRead, readingDate=readingDate)

        return redirect("/readingHistory")
    else:
        # gets all the book titles that the user has read
        books = db.execute("SELECT title FROM books WHERE id = :id", id=session["user_id"])
        return render_template("logReading.html", books=books)


@app.route("/about")
@login_required
def about():
    # renders the html for the about page
    return render_template("about.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
