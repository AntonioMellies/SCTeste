from DB.DB_Config import ConfigDB
from DB.DB_Connection import DB_Connection

class DB_SCTeste(DB_Connection):
    dbIntelligence = None

    def __init__(self, environment):
        self.dbIntelligence = ConfigDB().get_configurations(environment)
