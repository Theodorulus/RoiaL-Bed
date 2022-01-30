from tabnanny import check
from flask import (
    Blueprint, request, jsonify
)
from src.controllers.auth import login_required
import src.service.music_service as music_service

music_bp = Blueprint("music", __name__, url_prefix="/music")


@music_bp.route("/play/<song_identifier>", methods=["GET"])
@login_required
def play_music(song_identifier):

    query = music_service.play_music(song_identifier)
    if len(query) == 1:
        
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
        }), 404


@music_bp.route("/add", methods=["POST"])
@login_required
def add_music_to_db():

    if 'song_path' not in request.form:
        return jsonify({'status': 'Path is required.'}), 400
    song_path = request.form["song_path"]
    music_service.add_music_to_db(song_path)

    check = music_service.get_last_song()

    if check is None:
        return jsonify({
            'status': 'record not found.'
        }), 404

    else:
        return jsonify({
        'status': 'Song added.',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'song_path': check['song_path'],
            'active': check['active']
        }
    }), 200


@music_bp.route("/setalarm", methods=["POST"])
@login_required
def set_alarm():

    if 'start' not in request.form or 'song_id' not in request.form:
        return jsonify({'status': 'bad form.'}), 400
    song_id = request.form["song_id"]
    start = request.form["start"]
    music_service.set_alarm(song_id, start, 300)

    check = music_service.get_last_alarm()

    if check is None:
        return jsonify({
            'status': 'record not found.'
        }), 404

    else:
        return jsonify({
        'status': 'Added alarm.',
        'data': {
            'id': check['id'],
            'start': check['start'],
            'song_id': check['song_id'],
            'duration': check['duration']
        }
    }), 200