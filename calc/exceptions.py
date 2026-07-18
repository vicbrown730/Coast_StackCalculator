class BaseCSCException(Exception):
    def __init__(self, message, type):
        self.pc = 0
        self.type = type
        super().__init__(message)

class StackManagement(BaseCSCException):
    pass

class MathError(BaseCSCException):
    def __init__(self, message, type):
        super().__init__(message, type)
        self.type_list = ["除以0"]

class SyntaxFault(BaseCSCException):
    def __init__(self, message, type):
        super().__init__(message, type)