import aiohttp
from api.functions import * # pylint: disable=import-error,wildcard-import
from api.songs import songs # pylint: disable=import-error

async def searchArtists(query, limit): # pylint: disable=invalid-name
    """
    idk ;-;
    """
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"country": "IN", "page": 0, "secType": "artist", "type": "search", "keyword": query}) as resp: # pylint: disable=undefined-variable,line-too-long
            result = await resp.json()
            ids = []
            for i in range(0,int(limit)):
                try:
                    ids.append(result['gr'][0]['gd'][int(i)]['seo'])
                except (IndexError, TypeError):
                    pass
            if len(ids) == 0:
                return await noSearchResults() # pylint: disable=undefined-variable
            return await createJson(ids)

async def createJson(result): # pylint: disable=invalid-name
    """
    idk ;-;
    """
    final_json = []
    for seokey in result:
        data = {}
        async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
            async with ses.post(g_url, params = {"seokey": seokey, "type": "artistDetail"}) as resp: # pylint: disable=undefined-variable
                results = await resp.json()
                data['seokey'] = results['artist'][0]['seokey']
                data['artist_id'] = results['artist'][0]['artist_id']
                data['name'] = results['artist'][0]['name']
                data['song_count'] = results['artist'][0]['songs']
                data['album_count'] = results['artist'][0]['albums']
                data['favorite_count'] = results['artist'][0]['favorite_count']
                data['artist_url'] = f"https://gaana.com/artist/{data['seokey']}"
                data['images'] = {'urls': {}}
                data['images']['urls']['large_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_l") # pylint: disable=line-too-long
                data['images']['urls']['medium_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_m") # pylint: disable=line-too-long
                data['images']['urls']['small_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_s") # pylint: disable=line-too-long
                final_json.append(data)
    return final_json

async def createJsonSeo(result): # pylint: disable=invalid-name
    """
    idk;-;
    """
    final_json = []
    data = {}
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"seokey": result, "type": "artistDetail"}) as resp: # pylint: disable=undefined-variable
            results = await resp.json()
            try:
                data['artist_id'] = results['artist'][0]['artist_id']
            except (KeyError, TypeError):
                return await incorrectSeokey() # pylint: disable=undefined-variable
            data['name'] = results['artist'][0]['name']
            data['song_count'] = results['artist'][0]['songs']
            data['album_count'] = results['artist'][0]['albums']
            data['favorite_count'] = results['artist'][0]['favorite_count']
            data['artist_url'] = f"https://gaana.com/artist/{results['artist'][0]['seokey']}"
            data['images'] = {'urls': {}}
            data['images']['urls']['large_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_l") # pylint: disable=line-too-long
            data['images']['urls']['medium_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_m") # pylint: disable=line-too-long
            data['images']['urls']['small_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_s") # pylint: disable=line-too-long
            data['top_tracks'] = await top_tracks(data['artist_id'])
            final_json.append(data)
            return final_json

async def top_tracks(artist_id):
    """
    idk ;-;
    """
    seokeys = []
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"id": artist_id, "order": 0, "page": 0, "sortBy": "popularity", "type": "artistTrackList"}) as resp: # pylint: disable=undefined-variable,line-too-long
            results = await resp.json()
            for i, track in enumerate(results['entities']): # pylint: disable=unused-variable
                seokeys.append(track['seokey'])
            return await songs.createJson(seokeys)
