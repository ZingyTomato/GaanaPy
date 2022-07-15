import aiohttp

from api.functions import * # pylint: disable=wildcard-import,unused-wildcard-import,import-error
from api.songs import songs # pylint: disable=import-error

async def getTrending(language, limit): # pylint: disable=invalid-name
    """
    Gets the trending results
    """
    _headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Cookie": f"__ul={language};"
    }
    async with aiohttp.ClientSession(headers = _headers) as ses:
        async with ses.post(g_url, params = {"type": "miscTrendingSongs"}) as resp: # pylint: disable=undefined-variable
            result = await resp.json()
            ids = []
            for i in range(0, int(limit)):
                try:
                    ids.append(result['entities'][int(i)]['seokey'])
                except IndexError:
                    pass
            if len(ids) == 0:
                return await noSearchResults() # pylint: disable=undefined-variable
            return await songs.createJson(ids)
