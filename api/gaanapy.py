import asyncio
import aiohttp
from api.songs.songs import Songs
from api.albums.albums import Albums
from api.artists.artists import Artists
from api.trending.trending import Trending
from api.newreleases.newreleases import NewReleases
from api.charts.charts import Charts
from api.playlists.playlists import Playlists
from api import endpoints
from api.functions import Functions
from api.errors import Errors

class GaanaPy(Songs, Albums, Artists, Trending, NewReleases, Charts, Playlists):
    def __init__(self):
        self.aiohttp = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        self.api_endpoints = endpoints
        self.functions = Functions()
        self.errors = Errors()

    async def _safe_request(self, method: str, url: str, **kwargs) -> dict:
        try:
            if method == "GET":
                response = await self.aiohttp.get(url, **kwargs)
            else:
                response = await self.aiohttp.post(url, **kwargs)
            if response.status != 200:
                return await self.errors.no_results()
            result = await response.json()
            if not isinstance(result, dict):
                return await self.errors.no_results()
            return result
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError, TypeError):
            return await self.errors.no_results()
