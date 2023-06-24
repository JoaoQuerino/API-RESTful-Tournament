from repository.abstract_repository import AbstractRepository
from repository.team_dto import TeamDTO


class TeamRepository(AbstractRepository):

    def __init__(self):
        super().__init__(TeamDTO)

    def update(self, id, team: TeamDTO):
        team_current = self.find(id)
        team_current.name = team.name

        self._session.commit()
