from flask import Flask, request, redirect, jsonify, json
import json
from api.songs import songs
from api.albums import albums
from api.artists import artists
from api.trending import trending
from api.playlists import playlists
from api.recommend import recommend
from api.functions import *

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(page404())

@app.route('/', methods=['GET'])
def landing_page():
    return jsonify(errorMessage())

@app.route('/songs/search', methods=['GET'])
def search_results():

    query = request.args.get('query')
    limit = request.args.get('limit')

    if query is None:
         return jsonify(noResults())
    elif limit is None:
         result = songs.searchSong(query, 10)
    else:
         result = songs.searchSong(query, limit)

    return jsonify(result)

@app.route('/songs/info', methods=['GET'])
def id_results():

    query = request.args.get('seokey')

    if query is None:
         return jsonify(noResultsId())

    result = songs.createJsonSeo(query)

    return jsonify(result)

@app.route('/songs/recommend', methods=['GET'])
def recommend_results():

    track_id = request.args.get('track_id')
    limit = request.args.get('limit')

    if track_id is None:
         return jsonify(noResultsRecommendations())
    elif limit is None:
         result = recommend.createJsonRecommendations(track_id, 20)
    else:
         result = recommend.createJsonRecommendations(track_id, limit)

    return jsonify(result)

@app.route('/albums/search', methods=['GET'])
def search_album_results():

    query = request.args.get('query')
    limit = request.args.get('limit')

    if query is None:
         return jsonify(noResultsAlbums())
    elif limit is None:
         result = albums.searchAlbum(query, 10)
    else:
         result = albums.searchAlbum(query, limit)

    return jsonify(result)

@app.route('/artists/search', methods=['GET'])
def search_artists_results():

    query = request.args.get('query')
    limit = request.args.get('limit')

    if query is None:
         return jsonify(noResultsArtists())
    elif limit is None:
         result = artists.searchArtists(query, 10)
    else:
         result = artists.searchArtists(query, limit)

    return jsonify(result)

@app.route('/albums/info', methods=['GET'])
def id_albums_results():

    query = request.args.get('seokey')

    if query is None:
         return jsonify(noResultsAlbumId())

    result = albums.createJsonSeo(query)

    return jsonify(result)

@app.route('/artists/info', methods=['GET'])
def id_artists_results():

    query = request.args.get('seokey')

    if query is None:
         return jsonify(noResultsArtistId())

    result = artists.createJsonSeo(query)

    return jsonify(result)

@app.route('/trending', methods=['GET'])
def trending_results():

    lang = request.args.get('lang')
    limit = request.args.get('limit')

    if lang is None:
         return jsonify(noResultsTrending())
    elif limit is None:
         result = trending.getTrending(lang, 10)
    else:
         result = trending.getTrending(lang, limit)

    return jsonify(result)

@app.route('/playlists/info', methods=['GET'])
def playlists_results():

    seokey = request.args.get('seokey')

    if seokey is None:
         return jsonify(noResultsPlaylistId())

    result = playlists.getPlaylists(seokey)

    return jsonify(result)

if __name__ == "__main__":
    app.debug = False
    app.config['JSON_SORT_KEYS'] = False
    app.run(host='0.0.0.0', port=5000, use_reloader=False, threaded=True)
