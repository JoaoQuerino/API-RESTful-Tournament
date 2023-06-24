from flask_restx import Resource, Namespace, fields
from flask import request, abort, jsonify, send_file
from services.player_service import PlayerService
from services.team_service import TeamService
from endpoints.player_vo import PlayerVO


ns = Namespace('player', description="Namespace for player management")

player_model = ns.model('player', {
    'id': fields.Integer(required=True, description='Player ID'),
    'name': fields.String(required=True, description='Name Player'),
    'team_id': fields.Integer(required=True, description='Team ID'),
    'number': fields.Integer(required=True, description='Shirt number'),
})

player_expect_model = ns.model('player', {
    'name': fields.String(required=True, description='Name Player'),
    'team_id': fields.Integer(required=True, description='Team ID'),
    'number': fields.Integer(required=True, description='Shirt number'),
})

@ns.route('')
class PlayersEndpoint(Resource):

    @ns.response(200, "Success")
    def get(self):
        """
        Get all players.
        """
        return PlayerVO._toJsonFromPlayers(PlayerService().get_all())

    @ns.expect(player_expect_model)
    @ns.response(200, "Success")
    @ns.response(400, "Value Error")
    @ns.response(404, "Not found")
    @ns.response(409, "Conflict")
    def post(self):
        """
        Create a new player.
        """
        try:
            player = PlayerVO.fromJson(request.get_json())
        except BaseException as e:
            abort(400, str(e))

        if not TeamService().is_cadastred_team(player.team_id):
            abort(404, "Team not found")

        if not TeamService().is_avaliable_number(player.team_id, player.number):
            abort(409, "Conflict: Number not available in this team")

        PlayerService().save(player)
        return jsonify(success="Successfully registered player!")

    @ns.response(200, "Success")
    def delete(self):
        """
        Delete all players.
        """
        PlayerService().delete_all()

        return jsonify(success="All players have been successfully deleted!")


@ns.route('/<int:id>')
class PlayerEndpoint(Resource):

    @ns.response(200, "Success")
    def get(self, id):
        """
        Get player by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        try:
            player = PlayerService().get(id)
        except:
            abort(404, "Player not found")

        return player.toJson()

    @ns.expect(player_expect_model)
    @ns.response(200, "Success")
    @ns.response(400, "Value error")
    @ns.response(403, "Invalid identifier")
    @ns.response(404, "Not found")
    @ns.response(409, "Conflict")
    def put(self, id):
        """
        Update player by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        if not PlayerService().is_cadastred_player(id):
            abort(404, "Player not found")

        body = request.get_json()
        try:
            player = PlayerVO.fromJson(body)

            if not TeamService().is_cadastred_team(player.team_id):
                abort(404, "Team not found")

            if player.number != PlayerService().get(id).number and (
                not TeamService().is_avaliable_number(player.team_id, player.number)):
                abort(409, "Conflict: Number not available in this team")

            player = PlayerService().put(id, player)
        except BaseException as e:
            abort(400, str(e))

        return jsonify(success="Player updated successfully!")

    @ns.response(200, "Success")
    @ns.response(403, "Invalid identifier")
    @ns.response(404, "Not found")
    def delete(self, id):
        """
        Delete player by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        try:
            PlayerService().delete(id)
        except BaseException as e:
            abort(404, str(e))

        return jsonify(success="Player deleted successfully!")

@ns.route('/team/<int:id>')
class TeamEndpoint(Resource):

    @ns.response(200, "Success")
    @ns.response(403, "Invalid identifier")
    @ns.response(404, "Team not found")
    def get(self, id):
        """
        Get all players by team ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        if not TeamService().is_cadastred_team(id):
            abort(404, "Team not found")

        players = PlayerService().get_all_by_team(id)

        return PlayerVO._toJsonFromPlayers(players)