from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import Environment
from DB import DB_Config

# Configure environment witch based on type of the execute
environment = Environment.EnvironmentFunctions.get_environment()
dbSCTeste = DB_Config.ConfigDB().get_configurations(environment)

engine = create_engine(dbSCTeste.SCTESTE_URL_DATABASE,
                       convert_unicode=True,
                       connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
