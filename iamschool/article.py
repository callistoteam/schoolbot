from .group import Group
from .file import File

class Article():
    def __init__(self, data):
        self.id = None
        self.title = None
        self.organization_id = None
        self.organization_name = None
        self.organization_logo = None
        self.group = None
        self.content = None
        self.author = None
        self.like = None
        self.share = None
        self.scrap = None
        self.comment = None
        self.images = None
        self.videos = None
        self.files = None
        self.created_at = None
        self.updated_at = None
        self.deleted_at = None
        self.link = None
        self.date = None
        self.day = None

        if 'id' in data:
            self.id = data['id']

        if 'title' in data:
            self.title = data['title']

        if 'organization_id' in data:
            self.organization_id = data['organization_id']

        if 'organization_name' in data:
            self.organization_name = data['organization_name']

        if 'organization_logo' in data:
            self.organization_logo = data['organization_logo']

        if 'group_name' in data and 'group_id' in data:
            self.group = Group({'id' : data['group_id'], 'name' : data['group_name']})

        if 'content' in data:
            self.content = data['content']

        if 'author' in data:
            self.author = data['author']

        if 'like_count' in data:
            self.like = data['like_count']

        if 'share_count' in data:
            self.share = data['share_count']

        if 'scrap_count' in data:
            self.scrap = data['scrap_count']

        if 'comment_count' in data:
            self.comment = data['comment_count']

        if 'images' in data:
            self.images = data['images']

        if 'video' in data:
            self.videos = data['video']

        if 'files' in data and data['files'] != None:
            self.files = [File(file) for file in data['files']]

        if 'created_at' in data:
            self.created_at = data['created_at']

        if 'updated_at' in data:
            self.updated_at = data['updated_at']

        if 'deleted_at' in data:
            self.deleted_at = data['deleted_at']

        if 'view_link' in data:
            self.link = data['view_link']

        if 'local_date_of_pub_date' in data:
            self.date = data['local_date_of_pub_date']

        if 'day_of_week_of_pub_date' in data:
            self.day = data['day_of_week_of_pub_date']

