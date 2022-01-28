import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=["POST"])
def register():
    if 'username' not in request.form:
        return jsonify({'status': 'Username is required.'}), 400
    if 'password' not in request.form:
        return jsonify({'status': 'Password is required.'}), 400

    username = request.form['username']
    password = request.form['password']

    db = get_db()
    try:
        db.execute(
            """INSERT INTO users (username, password) 
            VALUES (?, ?)""",
            (username, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        return jsonify({'status': f'User {username} is already registered.'}), 409

    return jsonify({'status': 'User registered succesfully'}), 200


@auth_bp.route('/login', methods=["POST"])
def login():
    if 'username' not in request.form:
        return jsonify({'status': 'Username is required.'}), 400
    if 'password' not in request.form:
        return jsonify({'status': 'Password is required.'}), 400

    username = request.form['username']
    password = request.form['password']

    db = get_db()
    user = db.execute(
        """SELECT * 
        FROM users 
        WHERE username = ?""", 
        (username,)
    ).fetchone()

    if user is None:
        return jsonify({'status': 'User not found'}), 404
    elif not check_password_hash(user['password'], password):
        return jsonify({'status': 'Username of password is incorrect'}), 401

    session.clear()
    session['user_id'] = user['id']
    db.execute("UPDATE users SET active = 0 WHERE active = 1")
    db.execute("UPDATE users SET active = 1 WHERE id = ?", (user['id'],) )
    db.commit()
    return jsonify({'status': 'User logged in succesfully'}), 200


@auth_bp.route('/logout')
def logout():
    session.clear()
    return jsonify({'status': 'User logged out succesfully'}), 200


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'status': 'User is not authenticated'}), 401

        return view(**kwargs)

    return wrapped_view


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
