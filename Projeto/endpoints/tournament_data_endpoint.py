from flask_restx import Resource, Namespace, fields
from flask import request, abort, jsonify, send_file
from services.tournament_data_service import TournamentDataService
from services.team_service import TeamService
from endpoints.tournament_data_vo import TournamentDataVO


ns = Namespace('tournament', description="Namespace for tournaments data management")

tournament_model = ns.model('tournament', {
    'id': fields.Integer(required=True, description='Tournament by this team ID'),
    'name': fields.String(required=True, description='Tournament Name'),
    'team_id': fields.Integer(required=True, description='Team ID of team owner by this data'),
    'favor_goal': fields.Integer(required=True, description='Integer number of favor goal'),
    'against_goal': fields.Integer(required=True, description='Integer number of against goal'),
    'wins': fields.Integer(required=True, description='Integer number of wins'),
    'loses': fields.Integer(required=True, description='Integer number of loses'),
    'draws': fields.Integer(required=True, description='Integer number of draw'),
})

tournament_expect_model = ns.model('tournament', {
    'name': fields.String(required=True, description='Tournament Name'),
    'team_id': fields.Integer(required=True, description='Team ID of team owner by this data'),
    'favor_goal': fields.Integer(required=True, description='Integer number of favor goal'),
    'against_goal': fields.Integer(required=True, description='Integer number of against goal'),
    'wins': fields.Integer(required=True, description='Integer number of wins'),
    'loses': fields.Integer(required=True, description='Integer number of loses'),
    'draws': fields.Integer(required=True, description='Integer number of draw'),
})

@ns.route('')
class TournamentDatasEndpoint(Resource):

    @ns.response(200, "Success")
    def get(self):
        """
        Get all tournament data.
        """
        return TournamentDataVO._toJsonFromTournamentsData(TournamentDataService().get_all())

    @ns.expect(tournament_expect_model)
    @ns.response(200, "Success")
    @ns.response(400, "Value Error")
    @ns.response(404, "Not found")
    def post(self):
        """
        Create a new tournament data.
        """
        try:
            if not TournamentDataService().is_avaliable_tournament(request.get_json()['team_id'], request.get_json()['name']):
                abort(400, "The registration of data for this team in this tournament already exists")

            tournament_data = TournamentDataVO.fromJson(request.get_json())
        except BaseException as e:
            abort(404, str(e))

        TournamentDataService().save(tournament_data)
        return jsonify(success="Successfully registered tournament data!")

    @ns.response(200, "Success")
    def delete(self):
        """
        Delete all tournaments data.
        """
        TournamentDataService().delete_all()

        return jsonify(success="All tournaments data have been successfully deleted!")


@ns.route('/<int:id>')
class TournamentDataEndpoint(Resource):

    @ns.response(200, "Success")
    def get(self, id):
        """
        Get tournament data by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        try:
            tournament_data = TournamentDataService().get(id)
        except BaseException as e:
            abort(404, str(e))

        return tournament_data.toJson()

    @ns.expect(tournament_expect_model)
    @ns.response(200, "Success")
    @ns.response(400, "Value error")
    @ns.response(403, "Invalid identifier")
    @ns.response(404, "Tournament not found")
    @ns.response(404, "Number not available in this team")
    def put(self, id):
        """
        Update tournament data by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        try:
            _ = TournamentDataService().get(id)
        except IndexError:
            abort(404, "Tournament not found")

        body = request.get_json()
        try:
            tournament_data = TournamentDataVO.fromJson(body)

            if tournament_data.name != TournamentDataService().get(id).name and (
                not TournamentDataService().is_avaliable_tournament(tournament_data.team_id, tournament_data.name)):
                abort(404, "Number not available in this team")

            tournament_data = TournamentDataService().put(id, tournament_data)
        except BaseException as e:
            abort(400, str(e))

        return jsonify(success="Tournament updated successfully!")

    @ns.response(200, "Success")
    @ns.response(403, "Invalid identifier")
    @ns.response(404, "Tournament not found")
    def delete(self, id):
        """
        Delete tournament data by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        try:
            TournamentDataService().delete(id)
        except BaseException as e:
            abort(404, str(e))

        return jsonify(success="Tournament data deleted successfully!")

@ns.route('/team/<int:id>')
class TournamentDatasByTeamEndpoint(Resource):

    @ns.response(200, "Success")
    def get(self, id):
        """
        Get all tournaments data by team ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        if not TeamService().is_cadastred_team(id):
            abort(404, "Team not found")

        tournaments_data = TournamentDataService().get_all_by_team(id)

        return TournamentDataVO._toJsonFromTournamentsData(tournaments_data)

    @ns.response(200, "Success")
    def delete(self, id):
        """
        Delete all tournaments from a team.
        """
        TournamentDataService().delete_all_by_team(id)

        return jsonify(success="All tournaments from this team have been successfully deleted!")

@ns.route('/<string:name>')
class TournamentDatasByNameEndpoint(Resource):

    @ns.response(200, "Success")
    def get(self, name):
        """
        Get all tournaments data by name.
        """
        tournaments_data = TournamentDataService().get_all_by_name(name)

        if len(tournaments_data) == 0:
            abort(404, "Tournament not found with that name")

        return TournamentDataVO()._toJsonFromTournamentsData(tournaments_data)

    @ns.response(200, "Success")
    @ns.response(403, "Invalid identifier")
    @ns.response(404, "Tournament not found with that name")
    def delete(self, name):
        """
        Delete all tournaments data by name.
        """
        tournaments_data = TournamentDataService().get_all_by_name(name)

        if len(tournaments_data) == 0:
            abort(404, "Tournament not found with that name")

        TournamentDataService().delete_all_by_name(name)

        return jsonify(success="Tournament data deleted successfully!")
