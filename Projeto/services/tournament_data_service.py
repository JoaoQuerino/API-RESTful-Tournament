from endpoints.tournament_data_vo import TournamentDataVO
from repository.tournament_data_dto import TournamentDataDTO
from repository.team_repository import TeamRepository
from repository.tournament_data_repository import TournamentDataRepository
import os


class TournamentDataService():

    __team_repository = TeamRepository()
    __tournament_data_repository = TournamentDataRepository()

    def get(self, id):
        dto:TournamentDataDTO = self.__tournament_data_repository.find(id)
        if dto is None:
            raise IndexError("Tournament not found")
        
        return TournamentDataVO.fromDto(dto)

    def get_all_by_team(self, team_id):
        return self.__tournament_data_repository.find_all_by_team(team_id)

    def get_all_by_name(self, name):
        return self.__tournament_data_repository.find_all_by_name(name)

    def delete(self, id):
        tournament = self.__tournament_data_repository.find(id)
        if tournament is None:
            raise IndexError("Tournament not found") 
        
        self.__tournament_data_repository.delete(tournament)

    def delete_all(self):
        tournaments = self.get_all()
        for tournament in tournaments:
            self.delete(tournament.id)

    def delete_all_by_team(self, team_id):
        tournaments = self.__tournament_data_repository.find_all_by_team(team_id)
        for tournament in tournaments:
            self.delete(tournament.id)

    def delete_all_by_name(self, name):
        tournaments = self.__tournament_data_repository.find_all_by_name(name)
        for tournament in tournaments:
            self.delete(tournament.id)

    def get_all(self):
        vos = []
        dtos = self.__tournament_data_repository.find_all()
        for dto in dtos:
            vos.append(TournamentDataVO.fromDto(dto))
        
        return vos

    def save(self, tournament:TournamentDataVO):
        self.__tournament_data_repository.add(tournament.toDto())

    def put(self, id, tournament:TournamentDataVO):
        self.__tournament_data_repository.update(id, tournament.toDto())

    def is_avaliable_tournament(self, team_id, name):
        if TeamRepository().find(team_id) == None:
            raise ValueError("Team not found")
        tournaments = self.get_all_by_team(team_id)
        for tournament in tournaments:
            if tournament.name == name:
                return False
        return True
        
