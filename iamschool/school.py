from .enums import SchoolType

class School():
    def __init__(self, data):
        self.id = None
        self.name = None
        self.type = None
        self.address = None

        if 'name' in data:
            self.name = data['name']

        if 'instituteNo' in data:
            self.id = data['instituteNo']

        if 'type' in data:
            self.type = SchoolType(data['type'])

        if 'address' in data:
            self.address = data['address']
