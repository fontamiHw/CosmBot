# cosm_exception.py

class CosmException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"CosmException: {self.message}"