class Group():
    def __init__(self, data):
        self.id = None
        self.name = None

        if 'name' in data:
            self.name = data['name']

        if 'id' in data:
            self.id = data['id']
