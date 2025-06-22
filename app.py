from fastapi import FastAPI, Query
from fastapi.openapi.utils import get_openapi
from api.gaanapy import GaanaPy
from typing import Optional

app = FastAPI()
gaanapy = GaanaPy()

@app.get("/")
async def home():
    return {"Docs": "/docs", "Github": 'https://github.com/ZingyTomato/GaanaPy'}

@app.get("/songs/search/", summary="Search for songs.")
async def songs_search(query: str = Query(description="Name of the song to search for."), 
limit: Optional[int] = 10):

    result = await gaanapy.search_songs(query, limit)
    return result

@app.get("/songs/info/", summary="Retrieve detailed information on a song.")
async def songs_info(seokey: str = Query(description=
                                         "The `seokey` of the song. Example: `tyler-herro` in `https://gaana.com/song/tyler-herro`")):
    track_list = []
    track_list.append(seokey)
    song_info = await gaanapy.get_track_info(track_list)
    return song_info

@app.get("/albums/search/", summary="Search for albums.")
async def albums_search(query: str = Query(description=
                                           "Name of the album to search for."), limit: Optional[int] = 10):
    
    result = await gaanapy.search_albums(query, limit)
    return result

@app.get("/albums/info/", summary="Retrieve detailed information on an album.")
async def albums_info(seokey: str = Query(description=
                                          "The `seokey` of the album. Example: `tyler-herro` in `https://gaana.com/album/tyler-herro`")):
    album_list = []
    album_list.append(seokey)
    album_info = await gaanapy.get_album_info(album_list, True)
    return album_info

@app.get("/artists/search/", summary="Search for artists.")
async def artists_search(query: str = Query(description=
                                            "Name of the artist to search for."), limit: Optional[int] = 10):
    
    result = await gaanapy.search_artists(query, limit)
    return result

@app.get("/artists/info/", summary="Retrieve detailed information on an artist.")
async def artists_info(seokey: str = Query(description=
                                           "The `seokey` of the artist. Example, `ksi` in `https://gaana.com/artist/ksi`")) :
    artist_list = []
    artist_list.append(seokey)
    artist_info = await gaanapy.get_artist_info(artist_list, True)
    return artist_info

@app.get("/artists/similar/", summary="Retrieve similar artists based on a specific artist.")
async def artists_similar(artist_id: str = Query(description=
                                           "The `artist_id` of the artist. Example: {artist_ids: `3519085`}"), limit: Optional[int] = 10) :
    
    similar_artists = await gaanapy.get_similar_artists(artist_id, limit)
    return similar_artists

@app.get("/trending", summary="Retrieve trending songs across languages.")
async def get_trending(language: str = Query(description=
                                             "Available options: English, Hindi, Tamil, Punjabi etc."), limit: Optional[int] = 10):

    result = await gaanapy.get_trending(language, limit)
    return result

@app.get("/newreleases", summary="Retrieve newly released songs and albums across languages.")
async def get_new_releases(language: str = Query(description=
                                                 "Available options: English, Hindi, Tamil, Punjabi etc."), limit: Optional[int] = 10):
    
    result = await gaanapy.get_new_releases(language, limit)
    return result

@app.get("/charts", summary="Retrieve the current top charts (charts are just playlists).")
async def get_charts(limit: Optional[int] = 10):

    result = await gaanapy.get_charts(limit)
    return result

@app.get("/playlists/info/", summary="Retrieve detailed information on a playlist.")
async def playlists_info(seokey: str = Query(description=
                                             "The `seokey` of the playlist. Example: `gaana-dj-hindi-top-50-1` in `https://gaana.com/playlist/gaana-dj-hindi-top-50-1`")):
    
    playlist_info = await gaanapy.get_playlist_info(seokey)
    return playlist_info

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
            title="GaanaPy",
            version='0.0',
            description=" An unofficial Gaana API written in Python. https://github.com/ZingyTomato/GaanaPy",
            routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
    
app.openapi = custom_openapi