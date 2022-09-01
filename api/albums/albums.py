import requests
import json
from api import functions, endpoints
from api.songs import songs

def searchAlbum(query, limit):

  url = endpoints.search_albums_url + query
  response = requests.request("POST", url, headers=functions.headers).text.encode()

  result = json.loads(response)

  ids = []

  for i in range(0,int(limit)):
    try:
      ids.append(result['gr'][0]['gd'][int(i)]['seo'])
    except (IndexError, TypeError):
      pass

  if len(ids) == 0:
    return functions.noSearchResults()
  
  return createJson(ids)

def createJson(result):

    final_json = []

    for seokey in result:

      data = {}
      url = endpoints.album_details_url + seokey
      response = requests.request("POST", url, headers=functions.headers).text.encode()
      results = json.loads(response)

      data['seokey'] = results['album']['seokey']
      data['album_id'] = results['album']['album_id']
      data['title'] = results['album']['title']

      try:
        data['artists'] = functions.findArtistNames(results['album']['artist'])
        data['artist_seokeys'] = functions.findArtistSeoKeys(results['tracks'][0]['artist'])
        data['artist_ids'] = functions.findArtistIds(results['tracks'][0]['artist'])
      except (KeyError, IndexError):
        data['artists'] = ""
        data['artist_seokeys'] = ""
        data['artist_ids'] = ""
        
      data['duration'] = results['album']['duration']
      data['is_explicit'] = results['album']['parental_warning']
      data['language'] = results['album']['language']
      data['label'] = results['album']['recordlevel']
      data['track_count'] = results['album']['trackcount']

      try:
        data['release_date'] = results['album']['release_date']
      except:
        data['release_date'] = ""

      data['play_count'] = results['album']['al_play_ct']
      data['favorite_count'] = results['album']['favorite_count']
      data['album_url'] = f"https://gaana.com/album/{results['album']['seokey']}"

      data['images'] = {'urls': {}}

      data['images']['urls']['large_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_l.jpg")
      data['images']['urls']['medium_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_m.jpg")
      data['images']['urls']['small_artwork'] = (results['album']['artwork'])
 
      final_json.append(data)

    return final_json

def createJsonSeo(seokey):

    final_json = []

    seokeys = []

    data = {}
    url = endpoints.album_details_url + seokey
    response = requests.request("POST", url, headers=functions.headers).text.encode()
    results = json.loads(response)

    try:
      data['seokey'] = results['album']['seokey']
    except (KeyError, TypeError):
      return functions.incorrectSeokey()

    data['album_id'] = results['album']['album_id']
    data['title'] = results['album']['title']

    try:
      data['artists'] = functions.findArtistNames(results['album']['artist'])
      data['artist_seokeys'] = functions.findArtistSeoKeys(results['tracks'][0]['artist'])
      data['artist_ids'] = functions.findArtistIds(results['tracks'][0]['artist'])
    except (KeyError, IndexError):
      data['artists'] = ""
      data['artist_seokeys'] = ""
      data['artist_ids'] = ""
      
    data['duration'] = results['album']['duration']
    data['is_explicit'] = results['album']['parental_warning']
    data['language'] = results['album']['language']
    data['label'] = results['album']['recordlevel']
    data['track_count'] = results['album']['trackcount']
    data['release_date'] = results['album']['release_date']
    data['play_count'] = results['album']['al_play_ct']
    data['favorite_count'] = results['album']['favorite_count']
    data['album_url'] = f"https://gaana.com/album/{results['album']['seokey']}"

    data['images'] = {'urls': {}}

    data['images']['urls']['large_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_l.jpg")
    data['images']['urls']['medium_artwork'] = (results['album']['artwork']).replace("size_s.jpg", "size_m.jpg")
    data['images']['urls']['small_artwork'] = (results['album']['artwork'])
 
    try:
      for i in range(0,int(data['track_count'])):
        seokeys.append(results['tracks'][i]['seokey'])
    except IndexError:
      return functions.albumInactive()

    data['tracks'] = songs.createJson(seokeys)

    final_json.append(data)

    return final_json