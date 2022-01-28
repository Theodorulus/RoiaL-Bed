from datetime import datetime
import sqlite3
from flask import (
    Blueprint, request, jsonify
)
# from auth import login_required
from db import get_db
# from playsound import playsound

music_bp = Blueprint("music", __name__, url_prefix="/music")


@music_bp.route("/", methods=["GET"])
def base_route():
    return jsonify({
            'status': 'Base route.',
        }), 200


@music_bp.route("/play/<song_identifier>", methods=["GET"])
def play_music(song_identifier):
    db = get_db()

    if song_identifier.isnumeric():
        query = db.execute("select * from songs where id = ? " , (song_identifier,)).fetchall()
    else:
        query = db.execute("select * from songs where song_path = ? " , (song_identifier,)).fetchall()

    if len(query) == 1:
        # playsound(query[0][0])
        db.execute("update songs set active = 0 where active = 1")
        db.execute("update songs set active = 1 where id = ?", (query[0][0],))
        db.commit()
        
        return jsonify({
            'status': 'Playing song.',
            'data': {
                'id': query[0][0],
                'timestamp': query[0][1],
                'path': query[0][2]
            }
        }), 200

    else:
        return jsonify({
            'status': 'Could not find song.',
        }), 400


@music_bp.route("/add", methods=["POST"])
def add_music_to_db():
    db = get_db()

    song_path = request.form["song_path"]

    if not song_path:
        return jsonify({'status': 'path required.'}), 400

    db.execute("insert into songs(song_path) values(?)", (song_path,))
    db.commit()

    return jsonify({
            'status': 'Added song.',
            'data': {
                'path': song_path
        }
        }), 200


@music_bp.route("/setalarm", methods=["POST"])
def set_alarm():
    db = get_db()

    song_id = request.form["song_id"]
    start = request.form["start"]
    duration = 300  # seconds

    if not song_id or not start:
        return jsonify({'status': 'bad form.'}), 400

    query = db.execute("select * from songs where id = ? ", (song_id,)).fetchall()

    if len(query) == 1:
        db.execute("insert into alarms(start, duration, song_id) values(?,?,?)", (start, duration, song_id))
        db.commit()

        return jsonify({
                'status': 'Added alarm.',
                'data': {
                    'start': start,
                    'song id': song_id
            }
            }), 200

    else:
        return jsonify({'status': 'bad song id.'}), 400
