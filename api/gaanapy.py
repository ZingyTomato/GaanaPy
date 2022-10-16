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
        self.aiohttp = aiohttp.ClientSession()
        self.api_endpoints = endpoints
        self.functions = Functions()
        self.errors = Errors()
        self.info = False
    def __await__(self):
        return self.async_init().__await__()