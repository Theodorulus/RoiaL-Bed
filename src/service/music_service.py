from distutils.log import error
from flask import (
    Blueprint, request, jsonify
)
from db import get_db

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
        
    return query
        # return jsonify({
        #     'status': 'Playing song.',
        #     'data': {
        #         'id': query[0][0],
        #         'timestamp': query[0][1],
        #         'path': query[0][2]
        #     }
        # }), 200

    # else:
    #     return jsonify({
    #         'status': 'Could not find song.',
    #     }), 400


def add_music_to_db(song_path):
    db = get_db()

    # song_path = request.form["song_path"]

    # if not song_path:
    #     raise error
    #     return jsonify({'status': 'path required.'}), 400

    db.execute("insert into songs(song_path) values(?)", (song_path,))
    db.commit()

    
    # return jsonify({
    #         'status': 'Added song.',
    #         'data': {
    #             'path': song_path
    #     }
    #     }), 200

def get_last_song():
    check = get_db().execute(
        """SELECT *
        FROM songs
        ORDER BY TIMESTAMP DESC
        LIMIT 1"""
    ).fetchone()

    return check

def get_last_alarm():
    check = get_db().execute(
        """SELECT *
        FROM alarms
        ORDER BY id DESC
        LIMIT 1"""
    ).fetchone()

    return check

def set_alarm(song_id, start, duration):
    db = get_db()

    query = db.execute("select * from songs where id = ? ", (song_id,)).fetchall()

    if len(query) == 1:
        db.execute("insert into alarms(start, duration, song_id) values(?,?,?)", (start, duration, song_id))
        db.commit()

    #     return jsonify({
    #             'status': 'Added alarm.',
    #             'data': {
    #                 'start': start,
    #                 'song id': song_id
    #         }
    #         }), 200

    # else:
    #     return jsonify({'status': 'bad song id.'}), 400
