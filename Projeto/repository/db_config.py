from repository.base import Base
from sqlalchemy import create_engine

from repository.team_dto import TeamDTO
from repository.player_dto import PlayerDTO
from repository.tournament_data_dto import TournamentDataDTO

class DBConfig:    
    
    __instance = None #Private

    def __init__(self):
        if DBConfig.__instance is not None:
            raise Exception("This class is a singleton, use DB.create_engine")
        else:
            DBConfig.__instance = self
        self.engine = self.create_connection()
    
    def create_connection(self):
        #Connection String DB
        db_string = "postgresql://postgres:adm123@127.0.0.1:5433/postgres"
        conn = create_engine(db_string)

        Base.metadata.create_all(conn.engine)

        return conn
    
    @staticmethod
    def create():
        if DBConfig.__instance is None:
            DBConfig.__instance = DBConfig()
        
        return DBConfig.__instance