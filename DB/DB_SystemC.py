import sqlite3
from DB import DB_Config
from DB.DB_Connection import DB_Connection


class DB_SystemC(DB_Connection):
    dbSystemCConfig = None

    def __init__(self, environment):
        self.dbSystemCConfig = DB_Config.ConfigDB().get_configurations(environment)

    def getConnection(self):
        conn = sqlite3.connect(self.dbSystemCConfig.SystemC_URL_DATABASE)
        return conn
