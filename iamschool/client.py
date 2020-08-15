import aiohttp
import json

from .errors import HTTPException
from .school import School
from .article import Article
        
class AsyncClient():
    
    def __init__(self):
        self.endpoint = {
            "search" : "https://school.iamservice.net/api/intro/search?categoryNames=초등,중등,고등,기타,유치원&name=%s",
            "recent_article" : "https://school.iamservice.net/api/article/organization/%s?next_token=%s",
            "group_article" : "https://school.iamservice.net/api/article/organization/%s/group/%s?next_token=%s"
        }

    async def search_school(self, name : str):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint['search'] % name) as resp:
                if resp.status == 200: 
                    info = json.loads(await resp.text())
                    return [School(school) for school in info['data']['list']]
                else:
                    raise HTTPException(resp.status)

    async def fetch_recent_article(self, id : int, next : int = 0):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint['recent_article'] % (id, next)) as resp:
                if resp.status == 200: 
                    articles = await resp.json()
                    return [Article(article) for article in articles['articles']]
                else:
                    raise HTTPException(resp.status)

    async def fetch_group_article(self, id : int, group : int, next : int = 0):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint['group_article'] % (id, group, next)) as resp:
                if resp.status == 200: 
                    articles = await resp.json()
                    return [Article(article) for article in articles['articles']]
                else:
                    raise HTTPException(resp.status)

        
        
