class File:
    def __init__(self, data: dict):
        self.url = data.get("url")
        self.title = data.get("title")
