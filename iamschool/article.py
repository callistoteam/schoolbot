from .file import File
from .group import Group


class Article:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.title = data.get("title")

        self.organization_id = data.get("organization_id")
        self.organization_name = data.get("organization_name")
        self.organization_logo = data.get("organization_logo")
        self.group = (
            Group({"id": data["group_id"], "name": data["group_name"]})
            if "group_name" in data and "group_id" in data
            else None
        )

        self.content = data.get("content")
        self.author = data.get("author")

        self.like = data.get("like_count")
        self.share = data.get("share_count")
        self.scrap = data.get("scrap_count")
        self.comment = data.get("comment_count")

        self.images = data.get("images")
        self.videos = data.get("video")

        self.files = (
            [File(file) for file in data.get("files")] if data.get("files") else None
        )

        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")
        self.deleted_at = data.get("deleted_at")

        self.link = data.get("view_link")
        self.date = data.get("local_date_of_pub_date")
        self.day = data.get("day_of_week_of_pub_date")
