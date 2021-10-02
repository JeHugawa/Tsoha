from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT id, password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return render_template("error.html", message="Käyttäjää ei ole olemassa")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                return redirect("/")
            else:
                return render_template("error.html", message="Salasana ei täsmää")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", message="Salasanat ei täsmää")
        else:
           hash_value = generate_password_hash(password)
           sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
           db.session.execute(sql, {"username":username, "password":hash_value})
           db.session.commit()
           session["username"] = username 
           return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/b/<int:board_id>/<int:thread_id>", methods=["GET"])
def page(board_id, thread_id):
    if request.method == "GET":
        sql = "SELECT M.sent, M.message FROM message M"
        payload = db.session.execute(sql)
        return render_template("thread.html", messages=payload)
