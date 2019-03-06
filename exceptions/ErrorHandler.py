class ErrorHandler(Exception):

    def __init__(self, status_code=None, payload=None, program=None):pass

    def to_dict(self): pass
