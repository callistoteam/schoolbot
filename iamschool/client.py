import json

import aiohttp

from .article import Article
from .errors import HTTPException
from .school import School


class AsyncClient:
    BASE = "https://school.iamservice.net/api"

    async def request(self, endpoint: str, **kwargs) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE + endpoint, **kwargs) as resp:
                if resp.status != 200:
                    raise HTTPException(resp.status)

                return await resp.json(content_type=None)

    async def search_school(self, name: str) -> list:
        info = await self.request(
            "/intro/search", params={"categoryNames": "초등,중등,고등,기타,유치원", "name": name}
        )

        return [School(school) for school in info["data"]["list"]]

    async def fetch_recent_article(self, id: int, next: int = 0) -> list:
        articles = await self.request(
            f"/article/organization/{id}", params={"next_token": next}
        )

        return [Article(article) for article in articles["articles"]]

    async def fetch_group_article(self, id: int, group: int, next: int = 0) -> list:
        articles = await self.request(
            f"/article/organization/{id}/group/{group}", params={"next_token": next}
        )

        return [Article(article) for article in articles["articles"]]

