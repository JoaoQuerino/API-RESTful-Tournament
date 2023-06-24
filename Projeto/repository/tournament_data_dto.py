from sqlalchemy.orm import relationship
from repository.base import Base
from sqlalchemy import Column, Integer, Sequence, String

class TournamentDataDTO(Base):
    __tablename__ = 'tournament_data'
    id = Column(Integer, Sequence('seq_tournament_pk'), primary_key=True,
                 autoincrement=True)
    team_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    favor_goal = Column(Integer, nullable=False)
    against_goal = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    loses = Column(Integer, nullable=False)
    draws = Column(Integer, nullable=False)
