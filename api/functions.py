import base64
import time
from Crypto.Cipher import AES

g_url = "https://gaana.com/apiv2" # pylint: disable=invalid-name

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

async def page404():
    """
    Returns the json for a page 404
    """
    landing_info = {'ERROR': 'This URL does not exist. Double check the entered URL.'}
    return landing_info

async def page500():
    """
    Returns the json for a page 500
    """
    landing_info = {'ERROR': 'There seems to be an issue. Double check the URL parameters.'}
    return landing_info

async def noResults(): # pylint: disable=invalid-name
    """
    Returns the json for a no results page
    """
    landing_info = {'ERROR': 'Please enter a valid query! /songs/search?query=SONG_NAME&limit=LIMIT'} # pylint: disable=line-too-long
    return landing_info

async def noSearchResults(): # pylint: disable=invalid-name
    """
    Returns the json for a no search results page
    """
    landing_info = {'ERROR': 'Unable to find any results!'}
    return landing_info

async def noResultsAlbums(): # pylint: disable=invalid-name
    """
    Returns the json for a no results album page
    """
    landing_info = {'ERROR': 'Please enter a valid query! /albums/search?query=ALBUM_NAME'}
    return landing_info

async def noResultsArtists(): # pylint: disable=invalid-name
    """
    Returns the json for a no results artists page
    """
    landing_info = {'ERROR': 'Please enter a valid query! /artists/search?query=ARTIST_NAME'}
    return landing_info

async def noResultsTrending(): # pylint: disable=invalid-name
    """
    Returns the json for a no results trending page
    """
    landing_info = {'ERROR': 'Please enter a valid language! /trending?lang=LANGUAGE (LANGUAGE=English, Hindi etc.)'} # pylint: disable=line-too-long
    return landing_info

async def noResultsNewReleases(): # pylint: disable=invalid-name
    """
    Returns the json for a no results new releases page
    """
    landing_info = {'ERROR': 'Please enter a valid language! /newreleases?lang=LANGUAGE (LANGUAGE=English, Hindi etc.)'} # pylint: disable=line-too-long
    return landing_info

async def noResultsId(): # pylint: disable=invalid-name
    """
    Returns the json for a no results id page
    """
    landing_info = {'ERROR': 'Please enter a valid seokey! /songs/info?seokey=SEOKEY'}
    return landing_info

async def noResultsAlbumId(): # pylint: disable=invalid-name
    """
    Returns the json for a no results album id page
    """
    landing_info = {'ERROR': 'Please enter a valid seokey! /albums/info?seokey=SEOKEY'}
    return landing_info

async def noResultsArtistId(): # pylint: disable=invalid-name
    """
    Returns the json for a no results artists id page
    """
    landing_info = {'ERROR': 'Please enter a valid seokey! /artists/info?seokey=SEOKEY'}
    return landing_info

async def noResultsPlaylistId(): # pylint: disable=invalid-name
    """
    Returns the json for a no results playlist id page
    """
    landing_info = {'ERROR': 'Please enter a valid seokey! /playlists/info?seokey=SEOKEY'}
    return landing_info

async def noResultsRecommendations(): # pylint: disable=invalid-name
    """
    Returns the json for a no results recommendations page
    """
    landing_info = {'ERROR': 'Please enter a valid track ID! /songs/recommend?track_id=TRACK_ID'}
    return landing_info

async def incorrectSeokey(): # pylint: disable=invalid-name
    """
    Returns the json for an incorrect seokey page
    """
    landing_info = {'ERROR': 'Invalid Seokey!'}
    return landing_info

async def albumInactive(): # pylint: disable=invalid-name
    """
    Returns the json for an album inactive page
    """
    landing_info = {'ERROR':'Album is Inactive/Incorrect Album SEOKEY.'}
    return landing_info

async def trackInactive(): # pylint: disable=invalid-name
    """
    Returns the json for a track inactive page
    """
    landing_info = {'ERROR':'Track is Inactive/Incorrect Track ID.'}
    return landing_info

async def invalidInteger(): # pylint: disable=invalid-name
    """
    Returns the json for an invalid integer page
    """
    landing_info = {'ERROR':'Please enter a valid limit integer!'}
    return landing_info

async def decryptLink(link): # pylint: disable=invalid-name
    """
    Decrypts the given link
    """
    IV = 'asd!@#!@#@!12312'.encode('utf-8') # pylint: disable=invalid-name
    KEY = 'g@1n!(f1#r.0$)&%'.encode('utf-8') # pylint: disable=invalid-name
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    stream_url = await unpad((aes.decrypt(base64.b64decode(link))).decode('utf-8'))
    if "https://vodhlsgaana.akamaized.net" in stream_url:
        stream_url = stream_url.replace("96.mp4.master", "320.mp4.master")
        return stream_url
    return stream_url

async def unpad(s): # pylint: disable=invalid-name
    """
    idk ;-;
    """
    return s[0:-ord(s[-1])]

async def findArtistNames(results): # pylint: disable=invalid-name
    """
    Finds the artists name
    """
    artists = []
    for i in results:
        artists.append(i['name'])
    return ', '.join(artists)

async def findArtistSeoKeys(results): # pylint: disable=invalid-name
    """
    Finds the artists seokey
    """
    seokeys = []
    for i in results:
        seokeys.append(i['seokey'])
    return ', '.join(seokeys)

async def findGenres(results): # pylint: disable=invalid-name
    """
    Find genres
    """
    genres = []
    for i in results:
        try:
            genres.append(i['name'])
        except ValueError:
            return ""
    return ', '.join(genres)

async def formatTime(ms): # pylint: disable=invalid-name
    """
    Formats the given time
    """
    return time.strftime('%M:%S', time.gmtime(int(ms)))
