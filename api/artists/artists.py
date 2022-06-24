import requests
from json import JSONDecoder
import json
import time
from api.functions import *
from api.songs import songs

def searchArtists(query, limit):

  url = f"https://gaana.com/apiv2?country=IN&page=0&secType=artist&type=search&keyword={query}"

  response = requests.request("POST", url, headers=headers).text.encode()

  result = json.loads(response)

  ids = []

  for i in range(0,int(limit)):
    try:
      ids.append(result['gr'][0]['gd'][int(i)]['seo'])
    except (IndexError, TypeError):
      pass

  if len(ids) == 0:
    return noSearchResults()
  
  return createJson(ids)

def createJson(result):

    final_json = []

    for seokey in result:
      data = {}
      response = requests.request("POST", f"https://gaana.com/apiv2?seokey={seokey}&type=artistDetail", headers=headers).text.encode()
      results = json.loads(response)

      data['seokey'] = results['artist'][0]['seokey']
      data['artist_id'] = results['artist'][0]['artist_id']
      data['name'] = results['artist'][0]['name']
      data['song_count'] = results['artist'][0]['songs']
      data['album_count'] = results['artist'][0]['albums']
      data['favorite_count'] = results['artist'][0]['favorite_count']
      data['artist_url'] = f"https://gaana.com/artist/{data['seokey']}"

      data['images'] = {'urls': {}}

      data['images']['urls']['large_artwork'] = results['artist'][0]['atw'].replace("size_m", "size_l")
      data['images']['urls']['medium_artwork'] = results['artist'][0]['atw'].replace("size_m", "size_m")
      data['images']['urls']['small_artwork'] = results['artist'][0]['atw'].replace("size_m", "size_s")

      final_json.append(data)

    return final_json

def createJsonSeo(result):

    final_json = []

    data = {}
    response = requests.request("POST", f"https://gaana.com/apiv2?seokey={result}&type=artistDetail", headers=headers).text.encode()
    results = json.loads(response)

    try:
      data['artist_id'] = results['artist'][0]['artist_id']
    except (KeyError, TypeError):
      return incorrectSeokey()

    data['name'] = results['artist'][0]['name']
    data['song_count'] = results['artist'][0]['songs']
    data['album_count'] = results['artist'][0]['albums']
    data['favorite_count'] = results['artist'][0]['favorite_count']
    data['artist_url'] = f"https://gaana.com/artist/{results['artist'][0]['seokey']}"

    data['images'] = {'urls': {}}

    data['images']['urls']['large_artwork'] = results['artist'][0]['atw'].replace("size_m", "size_l")
    data['images']['urls']['medium_artwork'] = results['artist'][0]['atw'].replace("size_m", "size_m")
    data['images']['urls']['small_artwork'] = results['artist'][0]['atw'].replace("size_m", "size_s")

    data['top_tracks'] = top_tracks(data['artist_id'])
 
    final_json.append(data)

    return final_json

def top_tracks(artist_id):

    final_json = []

    seokeys = []

    response = requests.request("POST", f"https://gaana.com/apiv2?id={artist_id}&language=&order=0&page=0&sortBy=popularity&type=artistTrackList", headers=headers).text.encode()
    results = json.loads(response)

    for i,track in enumerate(results['entities']):
        seokeys.append(track['seokey'])

    return songs.createJson(seokeys)