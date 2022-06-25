from Crypto.Cipher import AES
import base64
import json
import time
from flask import jsonify

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

def errorMessage():
    
    landing_info = {
    'Search For Songs': '/songs/search?query=SONG_NAME', 
    'Limit Search Results': '/songs/search?query=SONG_NAME&limit=LIMIT', 
    'Get Song Info With SEOKEY': '/songs/info?seokey=SEOKEY', 
    'Get Related Tracks With TRACK_ID': '/songs/recommend?track_id=TRACK_ID', 
    'Limit Recommendations With TRACK_ID': '/songs/recommend?track_id=TRACK_ID&limit=LIMIT',
    'Search For Albums': '/albums/search?query=ALBUM_NAME',
    'Limit Album Results': '/albums/search?query=ALBUM_NAME&limit=LIMIT', 
    'Get Album Info With SEOKEY': '/albums/info?seokey=SEOKEY', 
    'Search For Artists': '/artists/search?query=ARTIST_NAME',
    'Limit Artist Results': '/artists/search?query=ARTIST_NAME&limit=LIMIT', 
    'Get Artist Info With SEOKEY': '/artists/info?seokey=SEOKEY', 
    'Get Playlist Info with SEOKEY': '/playlists/info?seokey=SEOKEY',
    'Get Trending Tracks': '/trending?lang=LANGUAGE (LANGUAGE=English, Hindi etc.)',
    'Limit Trending Tracks': '/trending?lang=LANGUAGE&limit=LIMIT',
    'Get New Releases': '/newreleases?lang=LANGUAGE (LANGUAGE=English, Hindi etc.)',
    'Limit New Releases': '/newreleases?lang=LANGUAGE&limit=LIMIT',
    'Github': "https://github.com/ZingyTomato/GaanaPy"
    }

    return landing_info

def page404():

    landing_info={'ERROR': 'This URL does not exist. Double check the entered URL.'}

    return landing_info

def page500():

    landing_info={'ERROR': 'There seems to be an issue. Double check the URL parameters.'}

    return landing_info

def noResults():

    landing_info={'ERROR': 'Please enter a valid query! /songs/search?query=SONG_NAME&limit=LIMIT'}

    return landing_info

def noSearchResults():

    landing_info={'ERROR': 'Unable to find any results!'}

    return landing_info

def noResultsAlbums():

    landing_info={'ERROR': 'Please enter a valid query! /albums/search?query=ALBUM_NAME'}

    return landing_info

def noResultsArtists():

    landing_info={'ERROR': 'Please enter a valid query! /artists/search?query=ARTIST_NAME'}

    return landing_info

def noResultsTrending():

    landing_info={'ERROR': 'Please enter a valid language! /trending?lang=LANGUAGE (LANGUAGE=English, Hindi etc.)'}

    return landing_info

def noResultsNewReleases():

    landing_info={'ERROR': 'Please enter a valid language! /newreleases?lang=LANGUAGE (LANGUAGE=English, Hindi etc.)'}

    return landing_info

def noResultsId():

    landing_info={'ERROR': 'Please enter a valid seokey! /songs/info?seokey=SEOKEY'}

    return landing_info

def noResultsAlbumId():

    landing_info={'ERROR': 'Please enter a valid seokey! /albums/info?seokey=SEOKEY'}

    return landing_info

def noResultsArtistId():

    landing_info={'ERROR': 'Please enter a valid seokey! /artists/info?seokey=SEOKEY'}

    return landing_info

def noResultsPlaylistId():

    landing_info={'ERROR': 'Please enter a valid seokey! /playlists/info?seokey=SEOKEY'}

    return landing_info

def noResultsRecommendations():

    landing_info={'ERROR': 'Please enter a valid track ID! /songs/recommend?track_id=TRACK_ID'}

    return landing_info

def incorrectSeokey():

    landing_info={'ERROR': 'Invalid Seokey!'}

    return landing_info

def albumInactive():

    landing_info = {'ERROR':'Album is Inactive/Incorrect Album SEOKEY.'}

    return landing_info

def trackInactive():

    landing_info = {'ERROR':'Track is Inactive/Incorrect Track ID.'}
        
    return landing_info

def invalidInteger():

    landing_info = {'ERROR':'Please enter a valid limit integer!'}
        
    return landing_info

def decryptLink(link):

   IV = 'asd!@#!@#@!12312'.encode('utf-8')
   KEY = 'g@1n!(f1#r.0$)&%'.encode('utf-8')
   aes = AES.new(KEY, AES.MODE_CBC, IV)
   stream_url = unpad((aes.decrypt(base64.b64decode(link))).decode('utf-8'))

   if "https://vodhlsgaana.akamaized.net" in stream_url:
     
     stream_url = stream_url.replace("96.mp4.master", "320.mp4.master")
     return stream_url
       
   return stream_url

def unpad(s): 
  return s[0:-ord(s[-1])]

def findArtistNames(results):

  artists = []

  for i in results:
    artists.append(i['name'])

  return ', '.join(artists)

def findArtistSeoKeys(results):

  seokeys = []

  for i in results:
    seokeys.append(i['seokey'])

  return ', '.join(seokeys)

def findGenres(results):  

  genres = []

  for i in results:
    try:
      genres.append(i['name'])
    except ValueError:
        return ""

  return ', '.join(genres)

def formatTime(ms):
  return time.strftime('%M:%S', time.gmtime(int(ms)))
