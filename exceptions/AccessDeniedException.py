from exceptions.ErrorHandler import  ErrorHandler

class AccessDeniedException(ErrorHandler):
    status_code = 403

    def __init__(self, status_code=None, payload=None,program=None):
        Exception.__init__(self)
        self.message = 'Acesso Negado'
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.program = program

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_cod'] = self.status_code
        rv['program'] = self.program
        return rv
