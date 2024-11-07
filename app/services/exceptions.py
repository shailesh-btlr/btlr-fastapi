class ServiceException(Exception):
    """Base exception for service errors."""


class NotFoundException(ServiceException):
    """Raised when a record is not found."""


class UserExperienceException(ServiceException):
    """Raised when a state machine error occurs."""
