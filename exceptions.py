class BaseException(Exception):
    def __init__(self, error_message, **kwargs):
        self.status_code = kwargs.get("status_code") or 500
        self.error_message = error_message

class RetrievingMangaException(BaseException):
    """When no manga can be retrieved throw a exception"""
    pass