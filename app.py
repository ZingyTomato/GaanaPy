import os

from fastapi.exceptions import HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, Request
import uvicorn

from api.songs import songs
from api.albums import albums
from api.artists import artists
from api.trending import trending
from api.playlists import playlists
from api.recommend import recommend
from api.newreleases import newreleases
from api.functions import * # pylint: disable=wildcard-import,unused-wildcard-import

app = FastAPI(title = "GaanaPy", description = "GaanaPy is an unofficial JSON API for Gaana, an Indian Music Streaming Service.") # pylint: disable=line-too-long

@app.route("/", include_in_schema = False)
async def redirect_to_docs(request: Request): # pylint: disable=unused-argument
    """
    Route that redirects to the docs page
    """
    return RedirectResponse(url = "/docs")

@app.exception_handler(HTTPException)
async def custom_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler cuz zingy needs one ;-;
    """
    if exc.status_code == 404:
        return JSONResponse(content = await page404())
    elif exc.status_code == 500:
        return JSONResponse(content = await page500())
    else:
        return await http_exception_handler(request, exc)

@app.get("/songs/recommend")
async def recommend_results(request: Request, track_id = None, limit = None): # pylint: disable=unused-argument
    """
    Get recommended songs, /songs/recommend
    """
    if track_id is None:
        return JSONResponse(content = await noResultsRecommendations())
    elif limit is None:
        result = await recommend.createJsonRecommendations(track_id, 20)
    else:
        result = await recommend.createJsonRecommendations(track_id, limit)
    return JSONResponse(content = result)

@app.get("/songs/search")
async def search_results(request: Request, query = None, limit = None): # pylint: disable=unused-argument
    """
    Search songs, /songs/search
    """
    if query is None:
        return JSONResponse(content = await noResults())
    elif limit is None:
        result = await songs.searchSong(query, 10)
    else:
        result = await songs.searchSong(query, limit)
    return JSONResponse(content = result)

@app.get("/songs/info")
async def id_results(request: Request, query = None): # pylint: disable=unused-argument
    """
    Get info about songs, /songs/info
    """
    if query is None:
        return JSONResponse(content = await noResultsId())
    result = await songs.createJsonSeo(query)
    return JSONResponse(content = result)

@app.get("/albums/search")
async def search_album_results(request: Request, query = None, limit = None): # pylint: disable=unused-argument
    """
    Search albums, /albums/search
    """
    if query is None:
        return JSONResponse(content = await noResultsAlbums())
    elif limit is None:
        result = await albums.searchAlbum(query, 10)
    else:
        result = await albums.searchAlbum(query, limit)
    return JSONResponse(content = result)

@app.get("/albums/info")
async def id_albums_results(request: Request, seokey = None): # pylint: disable=unused-argument
    """
    Get info about albums, /albums/info
    """
    if seokey is None:
        return JSONResponse(content = await noResultsAlbumId())
    result = await albums.createJsonSeo(seokey)
    return JSONResponse(content = result)

@app.get("/artists/search")
async def search_artists_results(request: Request, query = None, limit = None): # pylint: disable=unused-argument
    """
    Search artists, /artists/search
    """
    if query is None:
        return JSONResponse(content = await noResultsArtists())
    elif limit is None:
        result = await artists.searchArtists(query, 10)
    else:
        result = await artists.searchArtists(query, limit)
    return JSONResponse(content = result)

@app.get("/artists/info")
async def id_artists_results(request: Request, seokey = None): # pylint: disable=unused-argument
    """
    Get info about artists, /artists/info
    """
    if seokey is None:
        return JSONResponse(content = await noResultsArtistId())
    result = await artists.createJsonSeo(seokey)
    return JSONResponse(content = result)

@app.get("/trending")
async def trending_results(request: Request, lang = None, limit = None): # pylint: disable=unused-argument
    """
    Get trending results, /trending
    """
    if lang is None:
        return JSONResponse(content = await noResultsTrending())
    elif limit is None:
        result = await trending.getTrending(lang, 10)
    else:
        result = await trending.getTrending(lang, limit)
    return JSONResponse(content = result)

@app.get("/newreleases")
async def newreleases_results(request: Request, lang = None, limit = None): # pylint: disable=unused-argument
    """
    New releases results, /newreleases
    """
    if lang is None:
        return JSONResponse(content = await noResultsNewReleases())
    elif limit is None:
        result = await newreleases.getNewReleases(lang, 10)
    else:
        result = await newreleases.getNewReleases(lang, limit)
    return JSONResponse(content = result)

@app.get("/playlists/info")
async def playlists_results(request: Request, seokey = None): # pylint: disable=unused-argument
    """
    Gets info about playlists, /playlists/info
    """
    if seokey is None:
        return JSONResponse(content = await noResultsPlaylistId())
    result = await playlists.getPlaylists(seokey)
    return JSONResponse(content = result)

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = int(os.getenv("PORT", default = 5000))) # pylint: disable=invalid-envvar-default
