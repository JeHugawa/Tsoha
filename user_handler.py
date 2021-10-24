from app import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False    
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.id
            return True
        else:
             return False


def register(username, password, password2):
        if password != password2:
            return False
        else:
           hash_value = generate_password_hash(password)
           sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
           db.session.execute(sql, {"username":username, "password":hash_value})
           db.session.commit()
           session["username"] = username 
           return True


def logout():
    del session["username"]
    del session["user_id"]
