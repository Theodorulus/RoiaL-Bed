from flask import Blueprint
import src.models.status as status

example_endpoint = Blueprint('example_endpoint', __name__, template_folder='templates')

@example_endpoint.route("/tzanca",  methods=['GET'])
def tzanca():
    return status.get_status()