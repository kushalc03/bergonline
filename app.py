import os

from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('bergonline.db', check_same_thread=False)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Table of all menu items shown on original screen.
@app.route("/")
@login_required
def index():

    with conn: 
        cursor = conn.cursor()
        data = cursor.execute("SELECT * FROM menu_data")
    
    return render_template("index.html", data=data)

# Table of all meals in the today_meals database, which people add meals they ate to 
@app.route("/today")
@login_required
def today():
    with conn: 
        cursor = conn.cursor()
        data = cursor.execute("SELECT * FROM today_meals")

    return render_template("today.html", data=data)

# Discussion board, table of all posts in the discussion database
@app.route("/discussion")
@login_required
def discussion():
    with conn: 
        cursor = conn.cursor()
        data = cursor.execute("SELECT * FROM discussion")

    return render_template("discussion.html", data=data)

# Inputting into the today_meals database.
@app.route("/input", methods = ["GET", "POST"])
@login_required
def input():
    if request.method == "POST":
        # Getting the name / servings of the menu item
        name = request.form.get("name")
        servings = request.form.get("servings")

        # Ensure name was submitted
        if not request.form.get("name"):
            return apology("must provide name", 400)

        # Ensure servings were submitted
        elif not request.form.get("servings"):
            return apology("must provide servings", 400)

        with conn: 
            cursor = conn.cursor()

            # Get protein, carbs, fat, and calories data (if possible, otherwise apologize)
            protein = cursor.execute("SELECT protein FROM menu_data WHERE name LIKE ?", (name,))
            try:
                protein = protein.fetchone()[0]
            except TypeError:
                return apology("check your spelling", 400)

            carbs = cursor.execute("SELECT carbs FROM menu_data WHERE name LIKE ?", (name,)) 
            carbs = carbs.fetchone()[0]

            fat = cursor.execute("SELECT fat FROM menu_data WHERE name LIKE ?", (name,)) 
            fat = fat.fetchone()[0]

            calories = cursor.execute("SELECT calories FROM menu_data WHERE name LIKE ?", (name,))
            calories = calories.fetchone()[0]

            # Insert into today_meals database
            try:
                cursor.execute("INSERT INTO today_meals (name, calories, carbs, fat, protein, serving_size) VALUES (?, ?, ?, ?, ?, ?)", 
                              (name, str(round(float(calories) * float(servings),1)), str(round(float(carbs) * float(servings),1)), str(round(float(fat) * float(servings),1)), str(round(float(protein) * float(servings),1)), servings))
            except:
                return apology("input correct values", 400)

            conn.commit()

        return redirect("/input")
    else:
        return render_template("input.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match", 400)

        with conn:
            
            cursor = conn.cursor()

            # Ensure username does not already exist
            cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
            row = cursor.fetchone()
            if row is not None:
                return apology("username already exists", 400)

            # Insert username and password into database
            userpass = cursor.execute("INSERT or IGNORE INTO users (username, hash) VALUES (?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password"))))

            # Query database for username
            cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))

            # Remember which user has logged in
            session["user_id"] = cursor.fetchall()[0][0]

            conn.commit()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

# Get nutrition data from menu_data database given a name
@app.route("/nutrition", methods=["GET", "POST"])
@login_required
def nutrition():

    if request.method == "POST":

        name = request.form.get("name")

        if not request.form.get("name"):
            return apology("must provide name", 400)

        # Find the nutrition data of the menu item the user chooses
        with conn: 
            cursor = conn.cursor()
            search = cursor.execute("SELECT * FROM menu_data WHERE name LIKE ? ORDER BY name DESC LIMIT 1", (name,))

        # Redirect user to home page
        return render_template("index.html", data=search)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("nutrition.html")

# Insert a post into the discussion database to be shown in the discussion tab
@app.route("/post", methods=["GET", "POST"])
@login_required
def post():

    if request.method == "POST":

        post = request.form.get("post")

        if not request.form.get("post"):
            return apology("must provide post", 400)

        with conn: 
            cursor = conn.cursor()
            
            # Insert into the table
            cursor.execute("INSERT INTO discussion (post_submitted) VALUES (?)", (post,))
            conn.commit()

        # Redirect user back to post page
        return redirect("/post")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("post.html")

# See a meal's nutrition values (comprised of multiple menu items)
@app.route("/meals", methods=["GET", "POST"])
@login_required
def meals():

    if request.method == "POST":

        # Command to get data given names

        name = tuple(request.form.get("name").split(", ")) # comma separated

        if not request.form.get("name"):
            return apology("must provide name", 400)

        command = "SELECT * FROM menu_data WHERE"
        for i in name:
            command += " (name) LIKE \"" + i + "\" OR"

        command = command[0:-3] + "GROUP BY name;"


        # Find the menu items the user chooses
        with conn: 
            cursor = conn.cursor()
            try:
                search = cursor.execute(command)
            except:
                return apology("cannot find", 400)

        # Redirect user to home page
        return render_template("index.html", data=search)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("meals.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        with conn:
            
            cursor = conn.cursor()
        
            # Query database for username
            cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
            row = cursor.fetchone()

            # Ensure username exists and password is correct
            if row is None:
                return apology("invalid username", 400)
            if not (check_password_hash(row[2],request.form.get("password"))):
                return apology("invalid password", 400)

            cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
            session["user_id"] = cursor.fetchall()[0][0]

            conn.commit()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Logout
@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")