class ConfigDB:
    @staticmethod
    def get_configurations(environment):
        if environment == 'config.ProductionConfig':
            ret = ProductionConfigDB()
            return ret
        elif environment == 'config.DevelopmentConfig':
            ret = DevelopmentConfigDB()
            return ret
        elif environment == 'config.TestingConfig':
            return TestingConfigDB()


class VariablesConfigDB:
    # System A
    SystemA_IP = None
    SystemA_PORT = None
    SystemA_SID = None
    SystemA_USER = None
    SystemA_PASS = None
    SystemA_URL_DATABASE = None
    # System B
    SystemB_IP = None
    SystemB_PORT = None
    SystemB_SID = None
    SystemB_USER = None
    SystemB_PASS = None
    SystemB_URL_DATABASE = None
    # System C
    SystemC_IP = None
    SystemC_PORT = None
    SystemC_SID = None
    SystemC_USER = None
    SystemC_PASS = None
    SystemC_URL_DATABASE = None
    # SCTeste
    SCTESTE_URL_DATABASE = None


class ProductionConfigDB(VariablesConfigDB):
    def __init__(self):
        print("Production Start DATABASE")


class DevelopmentConfigDB(VariablesConfigDB):
    def __init__(self):
        print("Development Start DATABASE")
        # System A
        self.SystemA_URL_DATABASE = 'systemA.db'
        # System B
        self.SystemB_URL_DATABASE = 'systemB.db'
        # System C
        self.SystemC_URL_DATABASE = 'systemC.db'
        #SCTeste
        self.SCTESTE_URL_DATABASE = 'sqlite:///developer.db'

class TestingConfigDB(VariablesConfigDB):
    def __init__(self):
        print("Testing Start DATABASE")
