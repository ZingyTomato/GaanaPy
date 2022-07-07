import requests
from json import JSONDecoder
import json
import time
from api.functions import *

def getCharts(limit):
    
    url = f"https://gaana.com/apiv2?page=0&type=miscTopCharts"

    response = requests.request("POST", url, headers=headers).text.encode()

    results = json.loads(response)

    playlist_ids = []

    final_json = []

    track_count = results['count']

    for i in range(0,int(limit)):
      try:

        if results['entities'][int(i)]['entity_type'] == "PL":

          data = {}

          data['seokey'] = results['entities'][int(i)]['seokey']
          data['playlist_id'] = results['entities'][int(i)]['entity_id']
          data['title'] = results['entities'][int(i)]['name']
          data['language'] = results['entities'][int(i)]['language']
          data['favorite_count'] = results['entities'][int(i)]['favorite_count']
          data['is_explicit'] = results['entities'][int(i)]['entity_info'][6]['value']
          data['play_count'] = results['entities'][int(i)]['entity_info'][-1]['value']
          data['playlist_url'] = f"https://gaana.com/playlist/{data['seokey']}"

          data['images'] = {'urls': {}}

          data['images']['urls']['large_artwork'] = (results['entities'][int(i)]['atwj']).replace("size_m.jpg", "size_l.jpg")
          data['images']['urls']['medium_artwork'] = (results['entities'][int(i)]['atwj'])
          data['images']['urls']['small_artwork'] = (results['entities'][int(i)]['atwj']).replace("size_m.jpg", "size_s.jpg")

          final_json.append(data)

      except IndexError:
        pass

    return final_json

