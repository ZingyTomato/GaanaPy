import requests
import json
from api import functions, endpoints

def createJsonSimilarSongs(song_id, limit):
    
    final_json = []

    data = {}    
    url = endpoints.similar_songs_url + song_id
    response = requests.request("POST", url, headers=functions.headers).text.encode()
    
    try:
      results = json.loads(response)
    except json.decoder.JSONDecodeError:
      return functions.noSearchResults()

    try:
      limit = int(limit)
    except ValueError:
      limit = 10

    if int(limit) > int(results['count']):
      limit = results['count']
      
    for i in range(0, int(limit)):
    
      data = {}  

      try:
        data['seokey'] = results['tracks'][int(i)]['seokey']
      except (IndexError, TypeError, KeyError):
        return functions.trackInactive()
        
      data['track_id'] = results['tracks'][int(i)]['track_id']
      data['title'] = results['tracks'][int(i)]['track_title']
      data['artists'] = functions.findArtistNames(results['tracks'][int(i)]['artist'])
      data['artist_seokeys'] = functions.findArtistSeoKeys(results['tracks'][int(i)]['artist'])
      data['artist_ids'] = functions.findArtistIds(results['tracks'][int(i)]['artist'])
      data['album'] = results['tracks'][int(i)]['album_title']
      data['duration'] = results['tracks'][int(i)]['duration']
      data['genres'] = functions.findGenres(results['tracks'][int(i)]['gener'])
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

def createJsonSimilarAlbums(album_id, limit):
    
    final_json = []

    data = {}    
    url = endpoints.similar_albums_url + album_id
    response = requests.request("POST", url, headers=functions.headers).text.encode()
    
    try:
      results = json.loads(response)
    except json.decoder.JSONDecodeError:
      return functions.noSearchResults()

    try:
      limit = int(limit)
    except ValueError:
      limit = 10

    if int(limit) > int(results['count']):
      limit = results['count']
      
    for i in range(0, int(limit)):
    
      data = {}  

      try:
        data['seokey'] = results['album'][int(i)]['seokey']
      except (IndexError, TypeError, KeyError):
        pass
        
      data['album_id'] = results['album'][int(i)]['album_id']
      data['title'] = results['album'][int(i)]['title']
      data['artists'] = functions.findArtistNames(results['album'][int(i)]['artist'])
      data['artist_seokeys'] = functions.findArtistSeoKeys(results['album'][int(i)]['artist'])
      data['artist_ids'] = functions.findArtistIds(results['album'][int(i)]['artist'])
      data['duration'] = results['album'][int(i)]['duration']
      data['genres'] = functions.findGenres(results['album'][int(i)]['gener'])
      data['is_explicit'] = results['album'][int(i)]['parental_warning']
      data['language'] = results['album'][int(i)]['language']
      data['release_date'] = results['album'][int(i)]['trackcount']
      data['track_count'] = results['album'][int(i)]['release_date']
      data['album_url'] = f"https://gaana.com/album/{data['seokey']}"

      data['images'] = {'urls': {}}

      data['images']['urls']['large_artwork'] = (results['album'][int(i)]['atw']).replace("size_m.jpg", "size_l.jpg")
      data['images']['urls']['medium_artwork'] = (results['album'][int(i)]['atw'])
      data['images']['urls']['small_artwork'] = (results['album'][int(i)]['atw']).replace("size_m.jpg", "size_s.jpg")

      final_json.append(data)

    return final_json

def createJsonSimilarArtists(artist_id, limit):
    
    final_json = []

    data = {}    

    response = requests.request("POST", f"https://gaana.com/apiv2?apiPath=https://apiv2.gaana.com/player/similar-artists/{artist_id}&index=4&type=artistDetailSection", headers=functions.headers).text.encode()
    
    try:
      results = json.loads(response)
    except json.decoder.JSONDecodeError:
      return functions.noSearchResults()

    try:
      limit = int(limit)
    except ValueError:
      limit = 10

    if int(limit) > int(results['count']):
      limit = results['count']
      
    for i in range(0, int(limit)):
    
      data = {}  

      try:
        data['seokey'] = results['entities'][int(i)]['seokey']
      except (IndexError, TypeError, KeyError):
        pass
        
      data['artist_id'] = results['entities'][int(i)]['entity_id']
      data['name'] = results['entities'][int(i)]['name']
      data['track_count'] = results['entities'][int(i)]['entity_info'][1]['value']
      data['album_count'] = results['entities'][int(i)]['entity_info'][0]['value']
      data['favorite_count'] = results['entities'][int(i)]['favorite_count']
      data['artist_url'] = f"https://gaana.com/artists/{data['seokey'] }"

      data['images'] = {'urls': {}}

      data['images']['urls']['large_artwork'] = (results['entities'][int(i)]['atwj']).replace("size_m.jpg", "size_l.jpg")
      data['images']['urls']['medium_artwork'] = (results['entities'][int(i)]['atwj'])
      data['images']['urls']['small_artwork'] = (results['entities'][int(i)]['atwj']).replace("size_m.jpg", "size_s.jpg")

      final_json.append(data)

    return final_json