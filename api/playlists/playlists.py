import requests
import json
from api import functions, endpoints
from api.songs import songs

def getPlaylists(seokey):

  url = endpoints.playlist_details_url + seokey
  
  response = requests.request("POST", url, headers=functions.headers).text.encode()
  result = json.loads(response)

  ids = []

  final_json = []

  track_count = result['count']

  for i in range(0,int(track_count)):
    try:
      ids.append(result['tracks'][int(i)]['seokey'])
    except (IndexError, TypeError, KeyError):
      pass

  if len(ids) == 0:
    return functions.incorrectSeokey()

  return songs.createJson(ids)