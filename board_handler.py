from app import db
from flask import session


def board_info(board_id):
    sql = "SELECT name, description FROM boards WHERE id=:board_id"
    result = db.session.execute(sql, {"board_id":board_id})
    info = result.fetchone()
    return info


def board_threads(board_id):
    sql = "SELECT topic, board_id, id, sent FROM threads where board_id=:board_id ORDER BY id DESC"
    board = db.session.execute(sql, {"board_id":board_id})
    return board


def create_thread(board_id, topic, message):
    sql = "INSERT INTO threads (board_id, topic, sent) VALUES (:board_id, :topic, CURRENT_TIMESTAMP)"
    db.session.execute(sql, {"board_id":board_id, "topic":topic})
    db.session.commit()
    result = db.session.execute("SELECT ID FROM threads ORDER BY id DESC LIMIT 1")
    thread_id = result.fetchone()
    thread_id = thread_id[0]
    sql = "INSERT INTO message (thread_id, poster_id, sent, message) VALUES (:thread_id, :poster_id, CURRENT_TIMESTAMP, :message)"
    db.session.execute(sql, {"thread_id":thread_id, "poster_id":session["user_id"], "message":message})
    db.session.commit()
