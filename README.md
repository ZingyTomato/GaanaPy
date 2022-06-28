# 🎶 GaanaPy

GaanaPy is an unofficial JSON API for [`Gaana`](https://gaana.com), an Indian Music Streaming Service.

![image](https://user-images.githubusercontent.com/79736973/175231809-f79f07f7-7439-4ebe-a515-1448d0605b28.png)

# 📖 Table Of Contents

* [`🎧 Features`](#-features)
* [`👨‍🔧 Usage`](#-usage)
* [`💻 Local Development`](#-local-development)
* [`🏥 Contributing`](#-contributing)
* [`🐳 Docker Deployment`](#-docker-deployment)

## 🎧 **Features**

##### The API can get the following details for a specific track in JSON format (Other Options Include: Albums, Artists, Trending, New Releases and Playlists):
- **Track Name**
- **Track Duration**
- **Track Artwork**
- **Track URL**
- **Track Language**
- **Artist Name**
- **Artist Artwork**
- **Album Name**
- **Album URL**
- **Album Artwork**
- **Proxied m3u8 Stream URLS to avoid Geo-Restrictions**
- **Release Date**
- .... and a lot more!

```json
[
  {
    "seokey": "tyler-herro", 
    "album_seokey": "tyler-herro", 
    "track_id": "32408795", 
    "title": "Tyler Herro", 
    "artists": "Jack Harlow", 
    "artist_seokeys": "jack-harlow", 
    "artist_image": "https://proxy.nikomusic.tk/gn_img/artists/XYybzrb2gz/Yybzn4Bgb2/size_m_1607927137.webp", 
    "album": "Tyler Herro", 
    "duration": "02:36", 
    "genres": "Hip Hop", 
    "is_explicit": 1, 
    "language": "English", 
    "label": "Generation Now/Atlantic", 
    "release_date": "2020-10-22", 
    "play_count": "<100K", 
    "favorite_count": 202, 
    "song_url": "https://gaana.com/song/tyler-herro", 
    "album_url": "https://gaana.com/album/tyler-herro", 
    "images": {
      "urls": {
        "large_artwork": "https://proxy.nikomusic.tk/gn_img/albums/4Z9bqo3yQn/Z9bq2AG1Ky/size_l.jpg", 
        "medium_artwork": "https://proxy.nikomusic.tk/gn_img/albums/4Z9bqo3yQn/Z9bq2AG1Ky/size_m.jpg", 
        "small_artwork": "https://proxy.nikomusic.tk/gn_img/albums/4Z9bqo3yQn/Z9bq2AG1Ky/size_s.jpg"
      }
    }, 
    "stream_urls": {
      "urls": {
        "high_quality": "https://proxy.nikomusic.tk/songs/3/3487503/32408795/32408795_96.mp4.xvod/master.m3u8?sign=1656348416-98YDnDjQ4y-0-b2704a7cd93e281e0faeb8a39f8bf219", 
        "medium_quality": "https://proxy.nikomusic.tk/songs/3/3487503/32408795/32408795_64.mp4.xvod/master.m3u8?sign=1656348416-5pgvIPXchS-0-6225adbe477c8e2ce77c01909798ec08", 
        "low_quality": "https://proxy.nikomusic.tk/songs/3/3487503/32408795/32408795_16.mp4.xvod/master.m3u8?sign=1656348416-5pgvIPXchS-0-6225adbe477c8e2ce77c01909798ec08"
      }
    }
  }
]
```

## 👨‍🔧 **Usage**

##### **Search For Songs**: (Requires a search query, limit is optional)
```sh
https://api.nikomusic.tk/songs/search?query=<insert-query-here>&limit=<insert-limit-here, eg. 5>
```
**Example:** Create a GET request or navigate to `https://api.nikomusic.tk/songs/search?query=tyler herro` to get a JSON response of song results in return.

---
##### **Search For Albums**: (Requires a search query, limit is optional)
```sh
https://api.nikomusic.tk/albums/search?query=<insert-query-here>&limit=<insert-limit-here, eg. 5>
```
**Example:** Create a GET request or navigate to `https://api.nikomusic.tk/albums/search?query=all over the place` to get a JSON response of album results in return.

----
##### **Search For Artists**: (Requires a search query, limit is optional)
```sh
https://api.nikomusic.tk/artists/search?query=<insert-query-here>&limit=<insert-limit-here, eg. 5>
```
**Example:** Create a GET request or navigate to `https://api.nikomusic.tk/artists/search?query=KSI` to get a JSON response of arist results in return.

----
##### **Get Song Info**: (Requires a SEOKEY)
```sh
https://api.nikomusic.tk/songs/info?seokey=SEOKEY
```
**How do I find a song's seokey?:**

* In a URL, for example, `https://gaana.com/song/tyler-herro`, `tyler-herro` is the song's seokey.  
* Using [`Search For Songs`](#search-for-songs-requires-a-search-query-limit-is-optional), locate:
```json 
[
  {
    "seokey": "tyler-herro", 
  }
]
 ```

**Example:** Create a GET request or navigate to `https://api.nikomusic.tk/songs/info?seokey=tyler-herro` to get a JSON response of the song's info in return.

----
##### **Get Album Info**: (Requires a SEOKEY)
```sh
https://api.nikomusic.tk/albums/info?seokey=ALBUM_SEOKEY
```
**How do I find an albums's seokey?:**

* In a URL, for example, `https://gaana.com/album/tyler-herro`, `tyler-herro` is the albums's seokey.  
* Using [`Search For Albums`](#search-for-albums-requires-a-search-query-limit-is-optional), locate:
```json 
[
  {
    "seokey": "tyler-herro", 
  }
]
 ```
* Using [`Search For Songs`](#search-for-songs-requires-a-search-query-limit-is-optional), locate:
```json 
[
  {
    "album_seokey": "tyler-herro", 
  }
]
```

**Example:** Create a GET request or navigate to `https://api.nikomusic.tk/albums/info?seokey=tyler-herro` to get a JSON response of the song's info in return.

----
##### **Get Artist Info**: (Requires a SEOKEY)
```sh
https://api.nikomusic.tk/artists/info?seokey=SEOKEY
```
**How do I find an artists's seokey?:**

* In a URL, for example, `https://gaana.com/artist/jack-harlow`, `jack-harlow` is the song's seokey.  
* Using [`Search For Songs`](#search-for-songs-requires-a-search-query-limit-is-optional) or [`Search For Albums`](#search-for-albums-requires-a-search-query-limit-is-optional), locate:
```json 
[
  {
    "artist_seokeys": "jack-harlow", (There may be more than 1 seokey depending on the number of artists in the song.) 
  }
]
 ```

**Example:** Create a GET request or navigate to `https://api.nikomusic.tk/artists/info?seokey=jack-harlow` to get a JSON response of the artists's info in return.

----
##### **Get Playlist Info**: (Requires a SEOKEY)

```sh
https://api.nikomusic.tk/playlists/info?seokey=SEOKEY
```
**How do I find a playlists's seokey?:**

* In a URL, for example, `https://gaana.com/playlist/gaana-dj-gaana-international-top-50`, `gaana-dj-gaana-international-top-50` is the playlists's seokey. 


**Example:** Create a GET request or navigate to `https://api.nikomusic.tk/playlists/info?seokey=gaana-dj-gaana-international-top-50` to get a JSON response of the playlists's info in return.

----
##### **Get Trending Tracks**: (Requires a LANGUAGE)
```sh
https://api.nikomusic.tk/trending?lang=LANGUAGE
```
**Language Options:** English, Hindi, Punjabi, Telugu, Tamil etc. (Warning: Case Sensitive!). Defaults to Hindi if no language is provided or if an invalid language is entered.

**Example:** Create a GET request or navigate to `https://api.nikomusic.tk/trending?lang=English` to get a JSON response of the trending English songs in return.

----
##### **Get New Releases**: (Requires a LANGUAGE)
```sh
https://api.nikomusic.tk/newreleases?lang=LANGUAGE
```
**Language Options:** English, Hindi, Punjabi, Telugu, Tamil etc. (Warning: Case Sensitive!). Defaults to Hindi if no language is provided or if an invalid language is entered.

**Example:** Create a GET request or navigate to `https://api.nikomusic.tk/newreleases?lang=English` to get a JSON response of both new English songs and English albums in return.

## 💻 **Local Development**

Clone the Repository
```sh
$ git clone https://github.com/ZingyTomato/GaanaPy
```
Enter `/GaanaPy` and install all the requirements using
```sh
$ pip3 install -r requirements.txt
```
Run the app using
```sh
$ python3 app.py
```

Navigate to: `http://127.0.0.1:5000` to get started.

## **🐳 Docker Deployment**

Deploy the API locally using the following Docker-Compose stack: 

```
---
version: "2.1"
services:
  gaanapy:
    image: zingytomato/gaanapy:latest
    container_name: gaanapy
    ports:
      - 5000:5000 # External port can be changed 
    restart: unless-stopped
```

Navigate to: `http://HOST_IP:5000` to get started.

## 🏥 Contributing

Feel free to create an issue if you encounter any bugs or would like to suggest something!
