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
    sql = "SELECT id,name FROM boards"
    result = db.session.execute(sql)
    return render_template("index.html",boards=result)


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


@app.route("/<int:board_id>", methods=["GET"])
def board(board_id):
    if request.method == "GET":
        sql = "SELECT name, description FROM boards WHERE id=:id"
        info = db.session.execute(sql,{"id":board_id})
        sql = "SELECT topic, board_id, id, sent FROM threads where board_id=:board_id"
        result = db.session.execute(sql, {"board_id":board_id})
        return render_template("boards.html",board=result, metainfo=info)


@app.route("/<int:board_id>/<int:thread_id>", methods=["GET"])
def page(board_id, thread_id):
    if request.method == "GET":
        sql = "SELECT M.sent, M.message FROM message M WHERE M.thread_id=:thread_id"
        payload = db.session.execute(sql,{"thread_id":thread_id})
        return render_template("thread.html", messages=payload)
