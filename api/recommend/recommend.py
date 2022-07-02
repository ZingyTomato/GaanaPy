import requests
import json
from api.functions import *

def createJsonRecommendations(song_id, limit):
    
    final_json = []

    data = {}    
    response = requests.request("POST", f"https://gaana.com/apiv2?id={song_id}&type=songSimilar", headers=headers).text.encode()
    
    try:
      results = json.loads(response)
    except json.decoder.JSONDecodeError:
      return noSearchResults()
      
    for i in range(0, int(limit)):
    
      data = {}  

      try:
        data['seokey'] = results['tracks'][int(i)]['seokey']
      except IndexError:
        return trackInactive()
        
      data['track_id'] = results['tracks'][int(i)]['track_id']
      data['title'] = results['tracks'][int(i)]['track_title']
      data['artists'] = findArtistNames(results['tracks'][int(i)]['artist'])
      data['artist_seokeys'] = findArtistSeoKeys(results['tracks'][int(i)]['artist'])
      data['album'] = results['tracks'][int(i)]['album_title']
      data['duration'] = formatTime(results['tracks'][int(i)]['duration'])
      data['genres'] = findGenres(results['tracks'][int(i)]['gener'])
      data['is_explicit'] = results['tracks'][int(i)]['parental_warning']
      data['language'] = results['tracks'][int(i)]['language']
      data['release_date'] = results['tracks'][int(i)]['release_date']
      data['song_url'] = f"https://gaana.com/song/{results['tracks'][int(i)]['seokey']}"
      data['album_url'] = f"https://gaana.com/album/{results['tracks'][int(i)]['albumseokey']}"

      data['images'] = {'urls': {}}

      data['images']['urls']['large_artwork'] = (results['tracks'][int(i)]['artwork_large'].replace("http://", "https://"))
      data['images']['urls']['medium_artwork'] = (results['tracks'][int(i)]['artwork_web'].replace("http://", "https://"))
      data['images']['urls']['small_artwork'] = (results['tracks'][int(i)]['artwork'].replace("http://", "https://"))

      final_json.append(data)

    return final_json