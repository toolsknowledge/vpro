"""A single exception type that carries a student-friendly message and an HTTP status code."""


class ServiceError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
