import requests
from json import JSONDecoder
import json
import time
from api.functions import *
from api.songs import songs
from api.albums import albums

def getNewReleases(language, limit):

  url = f"https://gaana.com/apiv2?language={language}&page=0&type=miscNewRelease"

  response = requests.request("POST", url, headers=headers).text.encode()

  result = json.loads(response)

  album_ids = []

  track_ids = []

  for i in range(0,int(limit)):
    try:

      if result['entities'][int(i)]['entity_type'] == "AL":
        album_ids.append(result['entities'][int(i)]['seokey'])
        
      elif result['entities'][int(i)]['entity_type'] == "TR":
        track_ids.append(result['entities'][int(i)]['seokey'])

    except IndexError:
      pass

  if len(track_ids) and len(album_ids) == 0:
    return noSearchResults()

  data = {}

  data['tracks'] = songs.createJson(track_ids)

  data['albums'] = albums.createJson(album_ids)

  return data
