from datetime import datetime 
from repository.player_dto import PlayerDTO
from endpoints.validation import _is_text_empty_validation as name_validation
from repository.team_dto import TeamDTO

class TeamVO():
    
    def __init__(self):
        self.id = None
        self.name = ''

    @staticmethod
    def fromDto(dto:TeamDTO):
        vo = TeamVO()
        vo.id = dto.id
        vo.name = dto.name

        return vo

    @staticmethod
    def fromJson(json): 
        vo = TeamVO()
        vo.name = name_validation(json, 'name')

        return vo

    def toDto(self):
        dto = TeamDTO()
        dto.id = self.id
        dto.name = self.name

        return dto

    def toJson(self):
        return self.__dict__.copy()

    @staticmethod
    def _toJsonFromTeams(teams):
        jsonTeams = []
        for team in teams:
            jsonTeams.append(team.toJson())
        return jsonTeams