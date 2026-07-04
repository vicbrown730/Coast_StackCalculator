class BaseCSCException(Exception):
    def __init__(self, message):
        self.pc = 0
        super().__init__(message)

class StackManagement(BaseCSCException):
    pass

class ZeroDivision(BaseCSCException):
    pass