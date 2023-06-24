from repository.abstract_repository import AbstractRepository
from repository.player_dto import PlayerDTO
from endpoints.player_vo import PlayerVO


class PlayerRepository(AbstractRepository):

    def __init__(self):
        super().__init__(PlayerDTO)

    def update(self, id, player: PlayerDTO):
        player_current = self.find(id)
        player_current.name = player.name
        player_current.number = player.number
        player_current.team_id = player.team_id

        self._session.commit()

    def find_all_by_number(self, number):
        players = self._session.query(PlayerDTO)
        players_number = []

        for player in players:
            if(player.number == number):
                players_number.append(PlayerVO.fromDto(player))

        return players_number

    def find_all_by_team(self, team_id):
        players = self._session.query(PlayerDTO)
        team_players = []

        for player in players:
            if(player.team_id == team_id):
                team_players.append(PlayerVO.fromDto(player))

        return team_players
    
    def delete_all_by_team(self, team_id):
        self._session.query(PlayerDTO).filter(
            PlayerDTO.team_id == team_id).delete()
        self._session.commit()
