from flask import Flask, jsonify
from flask_restx import Api
from endpoints.team_endpoint import ns as ns_team
from endpoints.player_endpoint import ns as ns_player
from endpoints.tournament_data_endpoint import ns as ns_tournament_data

app = Flask(__name__)
api = Api(
    app=app,
    doc='/_docs',
    version='1.0.0',
    title='Control by tournaments APP API',
    description='API for control by tournaments, with teams and inside a team have players'
)

api.add_namespace(ns_team)
api.add_namespace(ns_player)
api.add_namespace(ns_tournament_data)

@app.errorhandler(400)
def _bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(403)
def _forbidden(e):
    return jsonify(error=str(e)), 403

@app.errorhandler(404)
def _not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(409)
def _conflict(e):
    return jsonify(error=str(e)), 409

@app.errorhandler(413)
def _payload_too_large(e):
    return jsonify(error=str(e)), 413

@app.errorhandler(500)
def _internal_server_error(e):
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)