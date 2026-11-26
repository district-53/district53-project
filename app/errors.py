class DomainError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(DomainError, ValueError):
    """Input breaks (bad stats, taken username, bad photo...)"""


class AlreadyRegistered(DomainError):
    """Signup for an account that already exists"""


class NotAllowed(DomainError):
    """The current user has not access to this action"""


class NotFound(DomainError):
    """The requested object does not exist"""


def register_error_handlers(app):
    @app.errorhandler(NotAllowed)
    def handle_not_allowed(error):
        return error.message, 403

    @app.errorhandler(NotFound)
    def handle_not_found(error):
        return error.message, 404