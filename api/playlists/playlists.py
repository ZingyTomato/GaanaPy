import aiohttp

from api.functions import * # pylint: disable=import-error,wildcard-import,unused-wildcard-import
from api.songs import songs # pylint: disable=import-error

async def getPlaylists(seokey): # pylint: disable=invalid-name
    """
    Gets playlists
    """
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"seokey": seokey, "type": "playlistDetail"}) as resp: # pylint: disable=undefined-variable
            result = await resp.json()
            ids = []
            track_count = result['count']
            for i in range(0,int(track_count)):
                try:
                    ids.append(result['tracks'][int(i)]['seokey'])
                except IndexError:
                    pass
            if len(ids) == 0:
                return await incorrectSeokey() # pylint: disable=undefined-variable
            return await songs.createJson(ids)
