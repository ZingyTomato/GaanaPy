import requests
import json
from api import functions, endpoints

def getCharts(limit):
    
    url = endpoints.charts_url
    response = requests.request("POST", url, headers=functions.headers).text.encode()
    results = json.loads(response)

    playlist_ids = []

    final_json = []

    track_count = results['count']

    try:
      limit = int(limit)
    except ValueError:
      limit = 10

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
      except (IndexError, TypeError, KeyError):
        pass

    return final_json