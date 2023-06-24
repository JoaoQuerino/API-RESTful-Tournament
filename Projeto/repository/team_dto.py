from sqlalchemy.orm import relationship
from repository.base import Base
from sqlalchemy import Column, Integer, Sequence, String

class TeamDTO(Base):
    __tablename__ = 'team'

    id = Column(Integer, Sequence('seq_team_pk'), primary_key=True,
                 autoincrement=True)
    name = Column(String, nullable=False)