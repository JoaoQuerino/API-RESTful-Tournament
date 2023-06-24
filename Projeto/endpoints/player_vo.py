from datetime import datetime 
from repository.player_dto import PlayerDTO
from endpoints.validation import _is_text_empty_validation as name_validation
from endpoints.validation import _is_non_negative_integer_validation as number_validation


class PlayerVO():
    
    def __init__(self):
        self.id = None
        self.name = ''
        self.number = None
        self.team_id = None
    
    @staticmethod
    def fromDto(dto:PlayerDTO):
        vo = PlayerVO()
        vo.id = dto.id
        vo.name = dto.name
        vo.number = dto.number
        vo.team_id = dto.team_id

        return vo

    @staticmethod
    def fromJson(json): 
        vo = PlayerVO()
        vo.name = name_validation(json, 'name')
        vo.number = number_validation(json, 'number')
        vo.team_id = number_validation(json, 'team_id')

        return vo

    def toDto(self):
        dto = PlayerDTO()
        dto.id = self.id
        dto.name = self.name
        dto.number = self.number
        dto.team_id = self.team_id

        return dto

    def toJson(self):
        return self.__dict__.copy()

    @staticmethod
    def _toJsonFromPlayers(players):
        jsonPlayers = []
        for player in players:
            jsonPlayers.append(player.toJson())
        return jsonPlayers