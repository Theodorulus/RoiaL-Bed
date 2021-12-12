from flask import Blueprint
import src.models.status as status
from db import get_db

example_endpoint = Blueprint('example_endpoint', __name__, template_folder='templates')

@example_endpoint.route("/tzanca",  methods=['GET'])
def tzanca():
    return status.get_status()


@example_endpoint.route("/dbTest", methods =['GET'] )
def dbTest():
    db = get_db()
    db.execute("INSERT INTO SONGS(song_path) VALUES(?)", ("test",))
    db.commit()
    return status.get_status()