"""A file with custom built exceptions"""


class NoMatchingDataError(Exception):
    """Custom built exception for No matching data."""
    pass


class ApiError(Exception):
    """Custom built exception for errors with the API."""
    pass
