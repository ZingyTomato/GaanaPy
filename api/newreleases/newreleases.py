import requests
import json
from api import functions, endpoints
from api.songs import songs
from api.albums import albums

def getNewReleases(language, limit):

  url = endpoints.new_releases_url + language
  response = requests.request("POST", url, headers=functions.headers).text.encode()

  result = json.loads(response)

  album_ids = []

  track_ids = []

  try:
    limit = int(limit)
  except ValueError:
    limit = 10

  for i in range(0,int(limit)):
    try:
      if result['entities'][int(i)]['entity_type'] == "AL":
        album_ids.append(result['entities'][int(i)]['seokey'])
      elif result['entities'][int(i)]['entity_type'] == "TR":
        track_ids.append(result['entities'][int(i)]['seokey'])
    except IndexError:
      pass

  if len(track_ids) and len(album_ids) == 0:
    return functions.noSearchResults()

  data = {}

  data['tracks'] = songs.createJson(track_ids)

  data['albums'] = albums.createJson(album_ids)

  return data