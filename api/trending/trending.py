import requests
import json
from api import functions, endpoints
from api.songs import songs

def getTrending(language, limit):

  url = endpoints.trending_url

  headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0',
  'Cookie': f'__ul={language};'
  }

  response = requests.request("POST", url, headers=headers).text.encode()

  result = json.loads(response)

  ids = []

  final_json = []

  for i in range(0,int(limit)):
    try:
      ids.append(result['entities'][int(i)]['seokey'])
    except IndexError:
      pass

  if len(ids) == 0:
    return functions.noSearchResults()

  return songs.createJson(ids)