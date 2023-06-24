from repository.abstract_repository import AbstractRepository
from repository.tournament_data_dto import TournamentDataDTO
from endpoints.tournament_data_vo import TournamentDataVO


class TournamentDataRepository(AbstractRepository):

    def __init__(self):
        super().__init__(TournamentDataDTO)

    def update(self, id, tournament_data: TournamentDataDTO):
        tournament_data_current = self.find(id)
        tournament_data_current.name = tournament_data.name
        tournament_data_current.team_id = tournament_data.team_id
        tournament_data_current.favor_goal = tournament_data.favor_goal
        tournament_data_current.against_goal = tournament_data.against_goal
        tournament_data_current.wins = tournament_data.wins
        tournament_data_current.loses = tournament_data.loses
        tournament_data_current.draws = tournament_data.draws

        self._session.commit()
    
    def find_all_by_team(self, team_id):
        tournaments_data = self._session.query(TournamentDataDTO)
        team_tournaments = []
        
        for tournament_data in tournaments_data:
            if(tournament_data.team_id == team_id):
                team_tournaments.append(
                    TournamentDataVO.fromDto(tournament_data))
        
        return team_tournaments
    
    def find_all_by_name(self, name):
        tournaments_data = self._session.query(TournamentDataDTO)
        team_tournaments = []
        
        for tournament_data in tournaments_data:
            if(tournament_data.name == name):
                team_tournaments.append(
                    TournamentDataVO.fromDto(tournament_data))

        return team_tournaments

    def delete_all_by_team(self, team_id):
        self._session.query(TournamentDataDTO).filter(
            TournamentDataDTO.team_id == team_id).delete()
        self._session.commit()

    def delete_all_by_name(self, name):
        self._session.query(TournamentDataDTO).filter(
            TournamentDataDTO.name == name).delete()
        self._session.commit()

