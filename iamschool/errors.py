import http

class HTTPException(Exception):
    def __init__(self, status):
        super().__init__(f"{status} {http.client.responses[status]}")