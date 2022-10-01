from flask import Flask, jsonify, request
from api.songs import songs
from api.albums import albums
from api.artists import artists
from api.trending import trending
from api.playlists import playlists
from api.similar import similar
from api.newreleases import newreleases
from api.charts import charts
from api import functions

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(functions.page404())

@app.errorhandler(500)
def page_not_found(e):
    return jsonify(functions.page500())

@app.route('/', methods=['GET'])
def landing_page():
    return jsonify(functions.errorMessage())

@app.route('/songs/search', methods=['GET'])
def search_results():

    query = request.args.get('query')
    limit = request.args.get('limit')

    if query is None:
         return jsonify(functions.noResults())
    elif limit is None:
         result = songs.searchSong(query, 10)
    else:
         result = songs.searchSong(query, limit)

    if result == []:
     return jsonify(functions.noSearchResults())
    
    return jsonify(result)

@app.route('/songs/info', methods=['GET'])
def id_results():

    query = request.args.get('seokey')

    if query is None:
         return jsonify(functions.noResultsId())

    result = songs.createJsonSeo(query)

    return jsonify(result)

@app.route('/songs/similar', methods=['GET'])
def recommend_songs_results():

    track_id = request.args.get('track_id')
    limit = request.args.get('limit')

    if track_id is None:
         return jsonify(functions.noResultsRecommendationsSongs())
    elif limit is None:
         result = similar.createJsonSimilarSongs(track_id, 20)
    else:
         result = similar.createJsonSimilarSongs(track_id, limit)

    if result == []:
     return jsonify(functions.noSimilarResults())

    return jsonify(result)

@app.route('/albums/similar', methods=['GET'])
def recommend_album_results():

    album_id = request.args.get('album_id')
    limit = request.args.get('limit')

    if album_id is None:
         return jsonify(functions.noResultsRecommendationsAlbums())
    elif limit is None:
         result = similar.createJsonSimilarAlbums(album_id, 10)
    else:
         result = similar.createJsonSimilarAlbums(album_id, limit)

    if result == []:
     return jsonify(functions.noSimilarResults())

    return jsonify(result)

@app.route('/artists/similar', methods=['GET'])
def recommend_artists_results():

    artist_id = request.args.get('artist_id')
    limit = request.args.get('limit')

    if artist_id is None:
         return jsonify(functions.noResultsRecommendationsArtists())
    elif limit is None:
         result = similar.createJsonSimilarArtists(artist_id, 10)
    else:
         result = similar.createJsonSimilarArtists(artist_id, limit)

    if result == []:
     return jsonify(functions.noSimilarResults())

    return jsonify(result)

@app.route('/albums/search', methods=['GET'])
def search_album_results():

    query = request.args.get('query')
    limit = request.args.get('limit')

    if query is None:
         return jsonify(functions.noResultsAlbums())
    elif limit is None:
         result = albums.searchAlbum(query, 10)
    else:
         result = albums.searchAlbum(query, limit)

    if result == []:
     return jsonify(functions.noSearchResults())

    return jsonify(result)

@app.route('/artists/search', methods=['GET'])
def search_artists_results():

    query = request.args.get('query')
    limit = request.args.get('limit')

    if query is None:
         return jsonify(functions.noResultsArtists())
    elif limit is None:
         result = artists.searchArtists(query, 10)
    else:
         result = artists.searchArtists(query, limit)

    if result == []:
     return jsonify(functions.noSearchResults())

    return jsonify(result)

@app.route('/albums/info', methods=['GET'])
def id_albums_results():

    query = request.args.get('seokey')

    if query is None:
         return jsonify(functions.noResultsAlbumId())

    result = albums.createJsonSeo(query)

    return jsonify(result)

@app.route('/artists/info', methods=['GET'])
def id_artists_results():

    query = request.args.get('seokey')

    if query is None:
         return jsonify(functions.noResultsArtistId())

    result = artists.createJsonSeo(query)

    return jsonify(result)

@app.route('/trending', methods=['GET'])
def trending_results():

    lang = request.args.get('lang')
    limit = request.args.get('limit')

    if lang is None:
         return jsonify(functions.noResultsTrending())
    elif limit is None:
         result = trending.getTrending(lang, 10)
    else:
         result = trending.getTrending(lang, limit)

    if result == []:
     return jsonify(functions.noTrending())

    return jsonify(result)

@app.route('/newreleases', methods=['GET'])
def newreleases_results():

    lang = request.args.get('lang')
    limit = request.args.get('limit')
  
    if lang is None:
         return jsonify(functions.noResultsNewReleases())
    elif limit is None:
         result = newreleases.getNewReleases(lang, 10)
    else:
         result = newreleases.getNewReleases(lang, limit)

    if result == []:
     return jsonify(functions.noNewReleases())

    return jsonify(result)

@app.route('/charts', methods=['GET'])
def charts_results():

    limit = request.args.get('limit')

    if limit is None:
         result = charts.getCharts(10)
    else:
         result = charts.getCharts(limit)

    if result == []:
     return jsonify(functions.noCharts())

    return jsonify(result)

@app.route('/playlists/info', methods=['GET'])
def playlists_results():

    seokey = request.args.get('seokey')

    if seokey is None:
         return jsonify(functions.noResultsPlaylistId())

    result = playlists.getPlaylists(seokey)

    return jsonify(result)

if __name__ == "__main__":
    app.debug = False
    app.config['JSON_SORT_KEYS'] = False
    app.run(host="0.0.0.0", port=5000, use_reloader=False, threaded=True)