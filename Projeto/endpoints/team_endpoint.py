from flask_restx import Resource, Namespace, fields
from flask import request, abort, jsonify, send_file
from services.team_service import TeamService
from endpoints.team_vo import TeamVO
import os
import shutil

ns = Namespace('team', description="Namespace for team management")

team_model = ns.model('team', {
    'id': fields.Integer(required=True, description='Team ID'),
    'name': fields.String(required=True, description='Name team'),
})

team_expect_model = ns.model('team', {
    'name': fields.String(required=True, description='Name team'),
})

@ns.route('')
class TeamsEndpoint(Resource):

    @ns.response(200, "Success")
    def get(self):
        """
        Get all teams.
        """
        return TeamVO._toJsonFromTeams(TeamService().get_all())

    @ns.expect(team_expect_model)
    @ns.response(200, "Success")
    @ns.response(400, "Value Error")
    def post(self):
        """
        Create a new team.
        """
        try:
            team = TeamVO.fromJson(request.get_json())
        except BaseException as e:
            abort(400, str(e))

        TeamService().save(team)
        return jsonify(success="Successfully registered team!")

    @ns.response(200, "Success")
    def delete(self):
        """
        Delete all teams.
        """
        TeamService().delete_all()

        return jsonify(success="All teams have been successfully deleted!")


@ns.route('/<int:id>')
class TeamEndpoint(Resource):

    @ns.response(200, "Success")
    def get(self, id):
        """
        Get team by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        try:
            team = TeamService().get(id)
        except:
            abort(404, "Team not found")

        return team.toJson()

    @ns.expect(team_expect_model)
    @ns.response(200, "Success")
    @ns.response(400, "Value error")
    @ns.response(403, "Invalid identifier")
    @ns.response(404, "Not found")
    def put(self, id):
        """
        Update team by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        body = request.get_json()
        try:
            team = TeamVO.fromJson(body)
            team = TeamService().put(id, team)
        except ValueError as e:
            abort(400, str(e))
        except BaseException as e:
            abort(404, str(e))

        return jsonify(success="Team successfully updated!")

    @ns.response(200, "Success")
    @ns.response(403, "Invalid identifier")
    @ns.response(404, "Not found")
    def delete(self, id):
        """
        Delete team by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")

        try:
            TeamService().delete(id)
        except BaseException as e:
            abort(404, str(e))

        return jsonify(success="Team deleted successfully!")


@ns.route('/<int:id>/logo')
class TeamLogoEndpoint(Resource):

    @ns.response(200, "Success")
    @ns.response(403, "Invalid identifier")
    def get(self, id):
        """
        Get team logo by ID.
        """
        if id < 1:
            abort(403, "Invalid identifier")
        try:
            TeamService().get(id)
            filename = TeamService().find_file(str(id))
            return send_file(filename, mimetype='image/jpeg')
        except IndexError or FileNotFoundError as e:
            abort(404, e)

    @ns.response(200, "Success")
    @ns.response(400, "Value error")
    @ns.response(403, "Invalid identifier")
    def post(self, id):
        """
        Upload team logo by ID.
        """
        try:
            if id < 1:
                abort(403, "Invalid identifier")

            if 'file' not in request.files:
                abort(400, "The logo is required")

            file = request.files['file']
            if file.filename.strip() == '' or not TeamService()._allowed_file(file.filename):
                abort(400, f"Invalid file, extension files are allowed: {TeamService().ALLOWED_EXTENSIONS}")

            blob = file.stream.read()
            
            if len(blob) == 0 or len(blob) / (1024 * 1024) > 32:
                abort(413, 'Invalid file size (Max. 32mb)')

            filename, extension = os.path.splitext(file.filename)
            if extension.startswith('.'):
                extension = extension[1:]

            filename = str(id) + '.' + extension

            file_path = os.path.join('/home/querino/Downloads/lab-dev-main/Projeto/FileLogos/ImagemTeste', filename)

            with open(file_path, 'wb') as file_image:
                file.stream.seek(0)
                shutil.copyfileobj(file.stream, file_image)

            return jsonify(success="Team logo added successfully!")
        except BaseException as e:
            abort(500, str(e))

            
