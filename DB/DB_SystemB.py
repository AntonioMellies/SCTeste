import sqlite3
from DB import DB_Config
from DB.DB_Connection import DB_Connection


class DB_SystemB(DB_Connection):
    dbSystemBConfig = None

    def __init__(self, environment):
        self.dbSystemBConfig = DB_Config.ConfigDB().get_configurations(environment)

    def getConnection(self):
        conn = sqlite3.connect(self.dbSystemBConfig.SystemB_URL_DATABASE)
        return conn
