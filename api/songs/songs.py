import aiohttp

from api.functions import * # pylint: disable=import-error,wildcard-import,unused-wildcard-import

async def searchSong(query, limit): # pylint: disable=invalid-name
    """
    idk ;-;
    """
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"country": "IN", "page": 0, "secType": "track", "type": "search", "keyword": query}) as resp: # pylint: disable=undefined-variable,line-too-long
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
            async with ses.post(g_url, params = {"seokey": seokey, "type": "songDetail"}) as resp: # pylint: disable=undefined-variable
                results = await resp.json()
                data['seokey'] = results['tracks'][0]['seokey']
                data['album_seokey'] = results['tracks'][0]['albumseokey']
                data['track_id'] = results['tracks'][0]['track_id']
                data['title'] = results['tracks'][0]['track_title']
                data['artists'] = await findArtistNames(results['tracks'][0]['artist']) # pylint: disable=undefined-variable
                data['artist_seokeys'] = await findArtistSeoKeys(results['tracks'][0]['artist']) # pylint: disable=undefined-variable
                data['artist_image'] = (results['tracks'][0]['artist_detail'][0]['atw'])
                data['album'] = results['tracks'][0]['album_title']
                data['duration'] = await formatTime(results['tracks'][0]['duration']) # pylint: disable=undefined-variable
                data['genres'] = await findGenres(results['tracks'][0]['gener']) # pylint: disable=undefined-variable
                data['is_explicit'] = results['tracks'][0]['parental_warning']
                data['language'] = results['tracks'][0]['language']
                data['label'] = results['tracks'][0]['vendor_name']
                data['release_date'] = results['tracks'][0]['release_date']
                data['play_count'] = results['tracks'][0]['play_ct']
                data['favorite_count'] = results['tracks'][0]['total_favourite_count']
                data['song_url'] = f"https://gaana.com/song/{data['seokey']}"
                data['album_url'] = f"https://gaana.com/album/{data['album_seokey']}"
                data['images'] = {'urls': {}}
                data['images']['urls']['large_artwork'] = (results['tracks'][0]['artwork_large'])
                data['images']['urls']['medium_artwork'] = (results['tracks'][0]['artwork_web'])
                data['images']['urls']['small_artwork'] = (results['tracks'][0]['artwork'])
                data['stream_urls'] = {'urls': {}}
                try:
                    data['stream_urls']['urls']['high_quality'] = (await decryptLink(results['tracks'][0]['urls']['high']['message'])) # pylint: disable=undefined-variable,line-too-long
                except KeyError:
                    data['stream_urls']['urls']['high_quality'] = ""
                data['stream_urls']['urls']['medium_quality'] = (await decryptLink(results['tracks'][0]['urls']['medium']['message'])) # pylint: disable=undefined-variable,line-too-long
                data['stream_urls']['urls']['low_quality'] = (await decryptLink(results['tracks'][0]['urls']['medium']['message'])).replace("64.mp4", "16.mp4") # pylint: disable=undefined-variable,line-too-long
                final_json.append(data)
    return final_json

async def createJsonSeo(seokey): # pylint: disable=invalid-name
    """
    idk ;-;
    """
    final_json = []
    data = {}
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"seokey": seokey, "type": "songDetail"}) as resp: # pylint: disable=undefined-variable
            results = await resp.json()
            try:
                data['track_id'] = results['tracks'][0]['track_id']
            except (TypeError, KeyError):
                return await incorrectSeokey() # pylint: disable=undefined-variable
            data['seokey'] = results['tracks'][0]['seokey']
            data['album_seokey'] = results['tracks'][0]['albumseokey']
            data['title'] = results['tracks'][0]['track_title']
            data['artists'] = await findArtistNames(results['tracks'][0]['artist']) # pylint: disable=undefined-variable
            data['artist_seokey'] = await findArtistSeoKeys(results['tracks'][0]['artist']) # pylint: disable=undefined-variable
            data['artist_image'] = (results['tracks'][0]['artist_detail'][0]['atw'])
            data['album'] = results['tracks'][0]['album_title']
            data['duration'] = await formatTime(results['tracks'][0]['duration']) # pylint: disable=undefined-variable
            data['genres'] = await findGenres(results['tracks'][0]['gener']) # pylint: disable=undefined-variable
            data['is_explicit'] = results['tracks'][0]['parental_warning']
            data['language'] = results['tracks'][0]['language']
            data['label'] = results['tracks'][0]['vendor_name']
            data['release_date'] = results['tracks'][0]['release_date']
            data['play_count'] = results['tracks'][0]['play_ct']
            data['favorite_count'] = results['tracks'][0]['total_favourite_count']
            data['song_url'] = f"https://gaana.com/song/{data['seokey']}"
            data['album_url'] = f"https://gaana.com/album/{data['album_seokey']}"
            data['images'] = {'urls': {}}
            data['images']['urls']['large_artwork'] = (results['tracks'][0]['artwork_large'])
            data['images']['urls']['medium_artwork'] = (results['tracks'][0]['artwork_web'])
            data['images']['urls']['small_artwork'] = (results['tracks'][0]['artwork'])
            data['stream_urls'] = {'urls': {}}
            try:
                data['stream_urls']['urls']['high_quality'] = (await decryptLink(results['tracks'][0]['urls']['high']['message'])) # pylint: disable=undefined-variable,line-too-long
            except KeyError:
                data['stream_urls']['urls']['high_quality'] = ""
            data['stream_urls']['urls']['medium_quality'] = (await decryptLink(results['tracks'][0]['urls']['medium']['message'])) # pylint: disable=undefined-variable,line-too-long
            data['stream_urls']['urls']['low_quality'] = (await decryptLink(results['tracks'][0]['urls']['medium']['message'])).replace("64.mp4", "16.mp4") # pylint: disable=undefined-variable, line-too-long
            final_json.append(data)
            return final_json
