import aiohttp

from api.functions import * # pylint: disable=import-error,wildcard-import
from api.songs import songs # pylint: disable=import-error

async def searchAlbum(query, limit): # pylint: disable=invalid-name
    """
    Search album function
    used to search albums
    """
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"country": "IN", "page": 0, "secType": "album", "type": "search", "keyword": query}) as resp: # pylint: disable=undefined-variable,line-too-long
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
            async with ses.post(g_url, params = {"seokey": seokey, "type": "albumDetail"}) as resp: # pylint: disable=undefined-variable
                results = await resp.json()
                data['seokey'] = results['album']['seokey']
                data['album_id'] = results['album']['album_id']
                data['title'] = results['album']['title']
                try:
                    data['artists'] = await findArtistNames(results['album']['artist']) # pylint: disable=undefined-variable
                    data['artist_seokeys'] = await findArtistSeoKeys(results['tracks'][0]['artist']) # pylint: disable=undefined-variable
                except (KeyError, IndexError): # idk y it still gives index error, also zingy if your seeing this FIX IT ;-;
                    data['artists'] = ""
                data['duration'] = await formatTime(results['album']['duration']) # pylint: disable=undefined-variable
                data['is_explicit'] = results['album']['parental_warning']
                data['language'] = results['album']['language']
                data['label'] = results['album']['recordlevel']
                data['track_count'] = results['album']['trackcount']
                try:
                    data['release_date'] = results['album']['release_date']
                except: # pylint: disable=bare-except
                    data['release_date'] = ""
                data['total_play_count'] = results['album']['al_play_ct']
                data['total_favorite_count'] = results['album']['favorite_count']
                data['album_url'] = f"https://gaana.com/album/{results['album']['seokey']}"
                data['images'] = {'urls': {}}
                data['images']['urls']['large_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_l.jpg") # pylint: disable=line-too-long
                data['images']['urls']['medium_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_m.jpg") # pylint: disable=line-too-long
                data['images']['urls']['small_artwork'] = (results['album']['artwork'])
                final_json.append(data)
                return final_json

async  def createJsonSeo(seokey): # pylint: disable=invalid-name
    """
    idk ;-;
    """
    final_json = []
    seokeys = []
    data = {}
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"seokey": seokey, "type": "albumDetail"}) as resp: # pylint: disable=undefined-variable
            results = await resp.json()
            try:
                data['seokey'] = results['album']['seokey']
            except (KeyError, TypeError):
                return await incorrectSeokey() # pylint: disable=undefined-variable
            data['album_id'] = results['album']['album_id']
            data['title'] = results['album']['title']
            try:
                data['artists'] = await findArtistNames(results['album']['artist']) # pylint: disable=undefined-variable
            except KeyError:
                data['artists'] = ""
            data['duration'] = await formatTime(results['album']['duration']) # pylint: disable=undefined-variable
            data['is_explicit'] = results['album']['parental_warning']
            data['language'] = results['album']['language']
            data['label'] = results['album']['recordlevel']
            data['track_count'] = results['album']['trackcount']
            data['release_date'] = results['album']['release_date']
            data['total_play_count'] = results['album']['al_play_ct']
            data['total_favorite_count'] = results['album']['favorite_count']
            data['album_url'] = f"https://gaana.com/album/{results['album']['seokey']}"
            data['images'] = {'urls': {}}
            data['images']['urls']['large_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_l.jpg") # pylint: disable=line-too-long
            data['images']['urls']['medium_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_m.jpg") # pylint: disable=line-too-long
            data['images']['urls']['small_artwork'] = (results['album']['artwork'])
            try:
                for i in range(0,int(data['track_count'])):
                    seokeys.append(results['tracks'][i]['seokey'])
            except IndexError:
                return await albumInactive() # pylint: disable=undefined-variable
            data['tracks'] = await songs.createJson(seokeys)
            final_json.append(data)
            return final_json
