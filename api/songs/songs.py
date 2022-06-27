import requests
from json import JSONDecoder
import json
import time
from api.functions import *

def searchSong(query, limit):

  url = f"https://gaana.com/apiv2?country=IN&page=0&secType=track&type=search&keyword={query}"

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
      response = requests.request("POST", f"https://gaana.com/apiv2?seokey={seokey}&type=songDetail", headers=headers).text.encode()
      results = json.loads(response)

      data['seokey'] = results['tracks'][0]['seokey']
      data['album_seokey'] = results['tracks'][0]['albumseokey']
      data['track_id'] = results['tracks'][0]['track_id']
      data['title'] = results['tracks'][0]['track_title']
      data['artists'] = findArtistNames(results['tracks'][0]['artist'])
      data['artist_seokeys'] = findArtistSeoKeys(results['tracks'][0]['artist'])
      data['artist_image'] = proxyUrl(results['tracks'][0]['artist_detail'][0]['atw'])
      data['album'] = results['tracks'][0]['album_title']
      data['duration'] = formatTime(results['tracks'][0]['duration'])
      data['genres'] = findGenres(results['tracks'][0]['gener'])
      data['is_explicit'] = results['tracks'][0]['parental_warning']
      data['language'] = results['tracks'][0]['language']
      data['label'] = results['tracks'][0]['vendor_name']
      data['release_date'] = results['tracks'][0]['release_date']
      data['play_count'] = results['tracks'][0]['play_ct']
      data['favorite_count'] = results['tracks'][0]['total_favourite_count']
      data['song_url'] = f"https://gaana.com/song/{data['seokey']}"
      data['album_url'] = f"https://gaana.com/album/{data['album_seokey']}"

      data['images'] = {'urls': {}}

      data['images']['urls']['large_artwork'] = proxyUrl(results['tracks'][0]['artwork_large'])
      data['images']['urls']['medium_artwork'] = proxyUrl(results['tracks'][0]['artwork_web'])
      data['images']['urls']['small_artwork'] = proxyUrl(results['tracks'][0]['artwork'])

      data['stream_urls'] = {'urls': {}}
   
      try:
        data['stream_urls']['urls']['high_quality'] = proxyUrl(decryptLink(results['tracks'][0]['urls']['high']['message']))
      except KeyError:
        data['stream_urls']['urls']['high_quality'] = ""
      
      data['stream_urls']['urls']['medium_quality'] = proxyUrl(decryptLink(results['tracks'][0]['urls']['medium']['message']))
      data['stream_urls']['urls']['low_quality'] = proxyUrl(decryptLink(results['tracks'][0]['urls']['medium']['message'])).replace("64.mp4", "16.mp4")

      final_json.append(data)

    return final_json

def createJsonSeo(seokey):

    final_json = []

    data = {}
    response = requests.request("POST", f"https://gaana.com/apiv2?seokey={seokey}&type=songDetail", headers=headers).text.encode()
    results = json.loads(response)

    try:
      data['track_id'] = results['tracks'][0]['track_id']
    except (TypeError, KeyError):
      return incorrectSeokey()

    data['seokey'] = results['tracks'][0]['seokey']
    data['album_seokey'] = results['tracks'][0]['albumseokey']
    data['title'] = results['tracks'][0]['track_title']
    data['artists'] = findArtistNames(results['tracks'][0]['artist'])
    data['artist_seokey'] = findArtistSeoKeys(results['tracks'][0]['artist'])
    data['artist_image'] = proxyUrl(results['tracks'][0]['artist_detail'][0]['atw'])
    data['album'] = results['tracks'][0]['album_title']
    data['duration'] = formatTime(results['tracks'][0]['duration'])
    data['genres'] = findGenres(results['tracks'][0]['gener'])
    data['is_explicit'] = results['tracks'][0]['parental_warning']
    data['language'] = results['tracks'][0]['language']
    data['label'] = results['tracks'][0]['vendor_name']
    data['release_date'] = results['tracks'][0]['release_date']
    data['play_count'] = results['tracks'][0]['play_ct']
    data['favorite_count'] = results['tracks'][0]['total_favourite_count']
    data['song_url'] = f"https://gaana.com/song/{data['seokey']}"
    data['album_url'] = f"https://gaana.com/album/{data['album_seokey']}"

    data['images'] = {'urls': {}}

    data['images']['urls']['large_artwork'] = proxyUrl(results['tracks'][0]['artwork_large'])
    data['images']['urls']['medium_artwork'] = proxyUrl(results['tracks'][0]['artwork_web'])
    data['images']['urls']['small_artwork'] = proxyUrl(results['tracks'][0]['artwork'])

    data['stream_urls'] = {'urls': {}}
   
    try:
      data['stream_urls']['urls']['high_quality'] = proxyUrl(decryptLink(results['tracks'][0]['urls']['high']['message']))
    except KeyError:
      data['stream_urls']['urls']['high_quality'] = ""
      
    data['stream_urls']['urls']['medium_quality'] = proxyUrl(decryptLink(results['tracks'][0]['urls']['medium']['message']))
    data['stream_urls']['urls']['low_quality'] = proxyUrl(decryptLink(results['tracks'][0]['urls']['medium']['message'])).replace("64.mp4", "16.mp4")

    final_json.append(data)

    return final_json
