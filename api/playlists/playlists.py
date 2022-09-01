import requests
import json
from api import functions
from api.songs import songs

def getPlaylists(seokey):

  url = f"https://gaana.com/apiv2?seokey={seokey}&type=playlistDetail"

  response = requests.request("POST", url, headers=functions.headers).text.encode()

  result = json.loads(response)

  ids = []

  final_json = []

  track_count = result['count']

  for i in range(0,int(track_count)):
    try:
      ids.append(result['tracks'][int(i)]['seokey'])
    except IndexError:
      pass

  if len(ids) == 0:
    return functions.incorrectSeokey()

  return songs.createJson(ids)