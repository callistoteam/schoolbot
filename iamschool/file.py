class File():
    def __init__(self, data):
        self.url = None
        self.title = None

        if 'url' in data:
            self.url = data['url']

        if 'title' in data:
            self.title = data['title']
