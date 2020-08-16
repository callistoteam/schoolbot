from .enums import SchoolType


class School:
    def __init__(self, data: dict):
        self.id = data.get("instituteNo")
        self.name = data.get("name")
        self.type = SchoolType(data["type"]) if "type" in data else None
        self.address = data.get("address")

