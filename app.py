from fastapi import FastAPI, Query, HTTPException, Depends, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.gaanapy import GaanaPy
from typing import Optional
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=502,
        content={"error": f"Upstream data source error: {type(exc).__name__}"}
    )
gaanapy = None

# Constants
MAX_LIMIT = 100
MIN_LIMIT = 1
DEFAULT_LIMIT = 10
MIN_PAGE = 1
DEFAULT_PAGE = 1
MAX_PAGE = 1000

MAX_QUERY_LENGTH = 200
MAX_SEOKEY_LENGTH = 200
MAX_ARTIST_ID_LENGTH = 20   
MAX_LANGUAGE_LENGTH = 50

SEO_KEY_BASE_PATTERN = r"^[a-z0-9\-]+$"                        # only lowercase, digits, hyphens
ARTIST_ID_PATTERN = r"^[0-9]+$"                                 # only digits
LANGUAGE_PATTERN = r"^[a-zA-Z]+(?:\s[a-zA-Z]+)*$"                # letters and single internal spaces,
                                                                  # no leading/trailing/blank-only input
SEARCH_QUERY_PATTERN = r"^[a-zA-Z0-9\s\-'.&]+$"

# Custom validator for seokey
def validate_seokey(
    seokey: str = Query(
        ...,
        min_length=1,
        max_length=MAX_SEOKEY_LENGTH,
        pattern=SEO_KEY_BASE_PATTERN,
        description="The `seokey` of the resource.",
    )
):
    if not re.search(r'[a-zA-Z]', seokey):
        raise HTTPException(status_code=400, detail="seokey must contain at least one alphabetic character")
    return seokey

@app.on_event("startup")
async def startup_event():
    global gaanapy
    gaanapy = GaanaPy()

@app.on_event("shutdown")
async def shutdown_event():
    if gaanapy and hasattr(gaanapy, 'aiohttp'):
        await gaanapy.aiohttp.close()

@app.get("/")
async def home():
    return {"Docs": "/docs", "Github": "https://github.com/ZingyTomato/GaanaPy"}

@app.get("/songs/search/", summary="Search for songs.")
async def songs_search(
    query: str = Query(..., min_length=1, max_length=MAX_QUERY_LENGTH,
                       pattern=SEARCH_QUERY_PATTERN,
                       description="Name of the song to search for."),
    limit: Optional[int] = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT, description="Number of results")
):
    result = await gaanapy.search_songs(query, limit)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/songs/info/", summary="Retrieve detailed information on a song.")
async def songs_info(
    seokey: str = Depends(validate_seokey)
):
    song_info = await gaanapy.get_track_info([seokey])
    if isinstance(song_info, dict) and "error" in song_info:
        raise HTTPException(status_code=404, detail=song_info["error"])
    return song_info

@app.get("/albums/search/", summary="Search for albums.")
async def albums_search(
    query: str = Query(..., min_length=1, max_length=MAX_QUERY_LENGTH,
                       pattern=SEARCH_QUERY_PATTERN,
                       description="Name of the album to search for."),
    limit: Optional[int] = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT)
):
    result = await gaanapy.search_albums(query, limit)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/albums/info/", summary="Retrieve detailed information on an album.")
async def albums_info(
    seokey: str = Depends(validate_seokey)
):
    album_info = await gaanapy.get_album_info([seokey], True)
    if isinstance(album_info, dict) and "error" in album_info:
        raise HTTPException(status_code=404, detail=album_info["error"])
    return album_info

@app.get("/artists/search/", summary="Search for artists.")
async def artists_search(
    query: str = Query(..., min_length=1, max_length=MAX_QUERY_LENGTH,
                       pattern=SEARCH_QUERY_PATTERN,
                       description="Name of the artist to search for."),
    limit: Optional[int] = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT)
):
    result = await gaanapy.search_artists(query, limit)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/artists/info/", summary="Retrieve detailed information on an artist.")
async def artists_info(
    seokey: str = Depends(validate_seokey),
    limit: Optional[int] = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT,
                                 description="Number of top tracks per page"),
    page: Optional[int] = Query(DEFAULT_PAGE, ge=MIN_PAGE, le=MAX_PAGE,
                                description="Page number for top tracks")
):
    artist_info = await gaanapy.get_artist_info([seokey], True, limit, page)
    if isinstance(artist_info, dict) and "error" in artist_info:
        raise HTTPException(status_code=404, detail=artist_info["error"])
    return artist_info

@app.get("/artists/similar/", summary="Retrieve similar artists based on a specific artist.")
async def artists_similar(
    artist_id: str = Query(..., min_length=1, max_length=MAX_ARTIST_ID_LENGTH,
                           pattern=ARTIST_ID_PATTERN,
                           description="The `artist_id` (numeric) of the artist. Example: `3519085`"),
    limit: Optional[int] = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT)
):
    similar_artists = await gaanapy.get_similar_artists(artist_id, limit)
    if isinstance(similar_artists, dict) and "error" in similar_artists:
        raise HTTPException(status_code=404, detail=similar_artists["error"])
    return similar_artists

@app.get("/trending", summary="Retrieve trending songs across languages.")
async def get_trending(
    language: str = Query(..., min_length=1, max_length=MAX_LANGUAGE_LENGTH,
                          pattern=LANGUAGE_PATTERN,
                          description="Available options: English, Hindi, Tamil, Punjabi etc."),
    limit: Optional[int] = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT)
):
    result = await gaanapy.get_trending(language, limit)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/newreleases", summary="Retrieve newly released songs and albums across languages.")
async def get_new_releases(
    language: str = Query(..., min_length=1, max_length=MAX_LANGUAGE_LENGTH,
                          pattern=LANGUAGE_PATTERN,
                          description="Available options: English, Hindi, Tamil, Punjabi etc."),
    limit: Optional[int] = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT)
):
    result = await gaanapy.get_new_releases(language, limit)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/charts", summary="Retrieve the current top charts (charts are just playlists).")
async def get_charts(
    limit: Optional[int] = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT)
):
    result = await gaanapy.get_charts(limit)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/playlists/info/", summary="Retrieve detailed information on a playlist.")
async def playlists_info(
    seokey: str = Depends(validate_seokey)
):
    playlist_info = await gaanapy.get_playlist_info(seokey)
    if isinstance(playlist_info, dict) and "error" in playlist_info:
        raise HTTPException(status_code=404, detail=playlist_info["error"])
    return playlist_info

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="GaanaPy",
        version='0.0',
        description="An unofficial Gaana API written in Python. https://github.com/ZingyTomato/GaanaPy",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi