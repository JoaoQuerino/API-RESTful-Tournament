from endpoints.team_vo import TeamVO
from repository.team_dto import TeamDTO
from repository.team_repository import TeamRepository
from repository.tournament_data_repository import TournamentDataRepository
from repository.player_repository import PlayerRepository
from services.player_service import PlayerService
import os


class TeamService():
    STORAGE_PATH = './FileLogos'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def _allowed_file(self, filename):
        return '.' in filename and \
            filename.split('.')[-1].lower() in self.ALLOWED_EXTENSIONS

    __team_repository = TeamRepository()
    __player_repository = PlayerRepository()
    __tournament_data_repository = TournamentDataRepository()

    def get(self, id):
        dto:TeamDTO = self.__team_repository.find(id)
        if dto is None:
            raise IndexError("Team not found")
        
        return TeamVO.fromDto(dto)

    def delete(self, id):
        team = self.__team_repository.find(id)
        if team is None:
            raise IndexError("Team not found") 
        
        self.__team_repository.delete(team)
        self.__player_repository.delete_all_by_team(id)
        self.__tournament_data_repository.delete_all_by_team(id)

    def delete_all(self):
        teams = self.get_all()
        for team in teams:  
            self.delete(team.id)

    def get_all(self):
        vos = []
        dtos = self.__team_repository.find_all()
        for dto in dtos:
            vos.append(TeamVO.fromDto(dto))
        
        return vos

    def find_file(self, name):
        for path, _, files in os.walk(self.STORAGE_PATH): 
            for filename in files:
                if name in filename:
                    return os.path.join(path, filename)
        raise FileNotFoundError('File not found')
    
    def save_file(self, id, file):
        blob = file.read()
        filename = str(id) + '.' + file.filename.split('.')[-1]
        file_image = open(os.path.join(self.STORAGE_PATH, filename), 'wb')
        file_image.write(blob)
        file_image.close()

    def save(self, team:TeamVO):
        self.__team_repository.add(team.toDto())

    def put(self, id, team:TeamVO):
        self.__team_repository.update(id, team.toDto())

    def is_cadastred_team(self, id):
        try:
            self.get(id)
        except:
            return False

        return True

    def is_avaliable_number(self, id, number):
        players = PlayerService().get_all_by_team(id)
        for player in players:
            if player.number == number:
                return False
        return True
        
