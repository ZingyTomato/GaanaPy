import requests
from json import JSONDecoder
import json
import time
from api.functions import *
from api.songs import songs

def getTrending(language, limit):

  url = "https://gaana.com/apiv2?type=miscTrendingSongs"

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

  return songs.createJson(ids)