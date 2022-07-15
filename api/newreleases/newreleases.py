import aiohttp

from api.functions import * # pylint: disable=import-error,wildcard-import,unused-wildcard-import
from api.songs import songs # pylint: disable=import-error
from api.albums import albums # pylint: disable=import-error

async def getNewReleases(language, limit): # pylint: disable=invalid-name
    """
    Gets the new releases
    """
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"language": language, "page": 0, "type": "miscNewRelease"}) as resp: # pylint: disable=undefined-variable,line-too-long
            result = await resp.json()
            album_ids = []
            track_ids = []
            for i in range(0, int(limit)):
                try:
                    if result['entities'][int(i)]['entity_type'] == "AL":
                        album_ids.append(result['entities'][int(i)]['seokey'])
                    elif result['entities'][int(i)]['entity_type'] == "TR":
                        track_ids.append(result['entities'][int(i)]['seokey'])
                except IndexError:
                    pass
            if len(track_ids) == 0 and len(album_ids) == 0: # pylint: disable=use-implicit-booleaness-not-len
                return await noSearchResults() # pylint: disable=undefined-variable
            data = {}
            data['tracks'] = await songs.createJson(track_ids)
            data['albums'] = await albums.createJson(album_ids)
            return data
