import aiohttp

from api.functions import * # pylint: disable=import-error,wildcard-import,unused-wildcard-import

async def createJsonRecommendations(song_id, limit): # pylint: disable=invalid-name
    """
    idk ;-;
    """
    final_json = []
    async with aiohttp.ClientSession(headers = headers) as ses: # pylint: disable=undefined-variable
        async with ses.post(g_url, params = {"id": song_id, "type": "songSimilar"}) as resp: # pylint: disable=undefined-variable
            try:
                results = await resp.json()
            except: # pylint: disable=bare-except
                return await noSearchResults() # pylint: disable=undefined-variable
            for i in range(0, int(limit)):
                data = {}
                try:
                    data['seokey'] = results['tracks'][int(i)]['seokey']
                except IndexError:
                    return await trackInactive() # pylint: disable=undefined-variable
                data['track_id'] = results['tracks'][int(i)]['track_id']
                data['title'] = results['tracks'][int(i)]['track_title']
                data['artists'] = await findArtistNames(results['tracks'][int(i)]['artist']) # pylint: disable=undefined-variable
                data['artist_seokeys'] = await findArtistSeoKeys(results['tracks'][int(i)]['artist']) # pylint: disable=undefined-variable,line-too-long
                data['album'] = results['tracks'][int(i)]['album_title']
                data['duration'] = await formatTime(results['tracks'][int(i)]['duration']) # pylint: disable=undefined-variable
                data['genres'] = await findGenres(results['tracks'][int(i)]['gener']) # pylint: disable=undefined-variable
                data['is_explicit'] = results['tracks'][int(i)]['parental_warning']
                data['language'] = results['tracks'][int(i)]['language']
                data['release_date'] = results['tracks'][int(i)]['release_date']
                data['song_url'] = f"https://gaana.com/song/{results['tracks'][int(i)]['seokey']}"
                data['album_url'] = f"https://gaana.com/album/{results['tracks'][int(i)]['albumseokey']}" # pylint: disable=line-too-long
                data['images'] = {'urls': {}}
                data['images']['urls']['large_artwork'] = (results['tracks'][int(i)]['artwork_large'].replace("http://", "https://")) # pylint: disable=line-too-long
                data['images']['urls']['medium_artwork'] = (results['tracks'][int(i)]['artwork_web'].replace("http://", "https://")) # pylint: disable=line-too-long
                data['images']['urls']['small_artwork'] = (results['tracks'][int(i)]['artwork'].replace("http://", "https://")) # pylint: disable=line-too-long
                final_json.append(data)
    return final_json
