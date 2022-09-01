import requests
import json
from api import functions, endpoints
from api.songs import songs

def searchArtists(query, limit):

  url = endpoints.search_artists_url + query
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
      url = endpoints.artist_details_url + seokey
      response = requests.request("POST", url, headers=functions.headers).text.encode()
      results = json.loads(response)

      data['seokey'] = results['artist'][0]['seokey']
      data['artist_id'] = results['artist'][0]['artist_id']
      data['name'] = results['artist'][0]['name']
      data['song_count'] = results['artist'][0]['songs']
      data['album_count'] = results['artist'][0]['albums']
      data['favorite_count'] = results['artist'][0]['favorite_count']
      data['artist_url'] = f"https://gaana.com/artist/{data['seokey']}"

      data['images'] = {'urls': {}}

      data['images']['urls']['large_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_l")
      data['images']['urls']['medium_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_m")
      data['images']['urls']['small_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_s")

      final_json.append(data)

    return final_json

def createJsonSeo(seokey):

    final_json = []

    data = {}
    url = endpoints.artist_details_url + seokey
    response = requests.request("POST", url, headers=functions.headers).text.encode()
    results = json.loads(response)

    try:
      data['artist_id'] = results['artist'][0]['artist_id']
    except (KeyError, TypeError):
      return functions.incorrectSeokey()

    data['name'] = results['artist'][0]['name']
    data['song_count'] = results['artist'][0]['songs']
    data['album_count'] = results['artist'][0]['albums']
    data['favorite_count'] = results['artist'][0]['favorite_count']
    data['artist_url'] = f"https://gaana.com/artist/{results['artist'][0]['seokey']}"

    data['images'] = {'urls': {}}

    data['images']['urls']['large_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_l")
    data['images']['urls']['medium_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_m")
    data['images']['urls']['small_artwork'] = (results['artist'][0]['atw']).replace("size_m", "size_s")

    data['top_tracks'] = top_tracks(data['artist_id'])
 
    final_json.append(data)

    return final_json

def top_tracks(artist_id):

    final_json = []

    seokeys = []

    url = endpoints.artist_top_tracks + artist_id
    response = requests.request("POST", url, headers=functions.headers).text.encode()
    results = json.loads(response)

    for i,track in enumerate(results['entities']):
        seokeys.append(track['seokey'])

    return songs.createJson(seokeys)