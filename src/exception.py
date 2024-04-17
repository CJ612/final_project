from fastapi import HTTPException, status



class RedirectException(HTTPException):
    def __init__(self, url: str):
        super().__init__(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT, detail="Temporary redirect"
        )
        self.headers = {"Location": url}

class NotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")