import sqlite3
from DB import DB_Config
from DB.DB_Connection import DB_Connection


class DB_SystemA(DB_Connection):
    dbSystemAConfig = None

    def __init__(self, environment):
        self.dbSystemAConfig = DB_Config.ConfigDB().get_configurations(environment)

    def getConnection(self):
        conn = sqlite3.connect(self.dbSystemAConfig.SystemA_URL_DATABASE)
        return conn
