from datetime import datetime 
from repository.tournament_data_dto import TournamentDataDTO
from endpoints.validation import _is_text_empty_validation as name_validation
from endpoints.validation import _is_non_negative_integer_validation


class TournamentDataVO():
    
    def __init__(self):
        self.id = None 
        self.team_id = None
        self.name = ''
        self.favor_goal = None
        self.against_goal = None
        self.wins = None
        self.loses = None
        self.draws = None

    @staticmethod
    def fromDto(dto:TournamentDataDTO):
        vo = TournamentDataVO()
        vo.id = dto.id
        vo.team_id = dto.team_id
        vo.name = dto.name
        vo.favor_goal = dto.favor_goal
        vo.against_goal = dto.against_goal
        vo.wins = dto.wins
        vo.loses = dto.loses
        vo.draws = dto.draws

        return vo

    @staticmethod
    def fromJson(json): 
        vo = TournamentDataVO()
        vo.team_id = _is_non_negative_integer_validation(json, 'team_id')
        vo.name = name_validation(json, 'name')
        vo.favor_goal = _is_non_negative_integer_validation(json, 'favor_goal')
        vo.against_goal = _is_non_negative_integer_validation(json, 'against_goal')
        vo.wins = _is_non_negative_integer_validation(json, 'wins')
        vo.loses = _is_non_negative_integer_validation(json, 'loses')
        vo.draws = _is_non_negative_integer_validation(json, 'draws')

        return vo

    def toDto(self):
        dto = TournamentDataDTO()
        dto.id = self.id
        dto.name = self.name
        dto.team_id = self.team_id
        dto.favor_goal = self.favor_goal
        dto.against_goal = self.against_goal
        dto.wins = self.wins
        dto.loses = self.loses
        dto.draws = self.draws

        return dto

    def toJson(self):
        return self.__dict__.copy()

    @staticmethod
    def _toJsonFromTournamentsData(tournaments_data):
        jsonTournamentsData = []
        for tournament_data in tournaments_data:
            jsonTournamentsData.append(tournament_data.toJson())
        return jsonTournamentsData