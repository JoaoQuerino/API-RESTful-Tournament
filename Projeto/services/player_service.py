from endpoints.player_vo import PlayerVO
from repository.player_dto import PlayerDTO
from repository.team_repository import TeamRepository
from repository.tournament_data_repository import TournamentDataRepository
from repository.player_repository import PlayerRepository
import os


class PlayerService():

    __team_repository = TeamRepository()
    __player_repository = PlayerRepository()
    __tournament_data_repository = TournamentDataRepository()

    def get(self, id):
        dto:PlayerDTO = self.__player_repository.find(id)
        if dto is None:
            raise IndexError("Player not found")
        
        return PlayerVO.fromDto(dto)

    def get_all_by_team(self, team_id):
        return self.__player_repository.find_all_by_team(team_id)

    def delete(self, id):
        player = self.__player_repository.find(id)
        if player is None:
            raise IndexError("Player not found") 
        
        self.__player_repository.delete(player)

    def delete_all(self):
        players = self.get_all()
        for player in players:
            self.delete(player.id)

    def get_all(self):
        vos = []
        dtos = self.__player_repository.find_all()
        for dto in dtos:
            vos.append(PlayerVO.fromDto(dto))
        
        return vos

    def save(self, player:PlayerVO):
        self.__player_repository.add(player.toDto())

    def put(self, id, player:PlayerVO):
        self.__player_repository.update(id, player.toDto())

    def is_cadastred_player(self, id):
        try:
            self.get(id)
        except:
            return False

        return True
