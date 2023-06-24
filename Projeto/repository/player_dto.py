from sqlalchemy.orm import relationship
from repository.base import Base
from sqlalchemy import Column, Integer, Sequence, String

class PlayerDTO(Base):
    __tablename__ = 'player'

    id = Column(Integer, Sequence('seq_player_pk'), primary_key=True,
                 autoincrement=True)
    name = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    team_id = Column(Integer, nullable=False)