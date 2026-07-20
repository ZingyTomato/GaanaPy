# GaanaPy

An unofficial JSON API for [Gaana](https://gaana.com), an Indian music streaming service. Built with FastAPI.

## Usage

Start the server (see [Local Development](#local-development)), then open the interactive docs:

http://127.0.0.1:8000/docs

### Endpoints

All endpoints return JSON. Search endpoints accept an optional `limit` (1–100, default 10).

| Endpoint | Description | Required |
|---|---|---|
| `GET /songs/search?query=` | Search songs | `query` |
| `GET /songs/info?seokey=` | Song details | `seokey` |
| `GET /albums/search?query=` | Search albums | `query` |
| `GET /albums/info?seokey=` | Album details (includes tracks) | `seokey` |
| `GET /artists/search?query=` | Search artists | `query` |
| `GET /artists/info?seokey=` | Artist details (with top tracks) | `seokey` |
| `GET /artists/similar?artist_id=` | Similar artists | `artist_id` |
| `GET /trending?language=` | Trending tracks | `language` |
| `GET /newreleases?language=` | New releases | `language` |
| `GET /charts` | Top chart playlists | — |
| `GET /playlists/info?seokey=` | Playlist details (with tracks) | `seokey` |
| `GET /health` | Health check | — |

### Language

`English`, `Hindi`, `Punjabi`, `Tamil`, `Telugu` etc. Case-sensitive.

### Finding a seokey

A **seokey** is the URL-friendly identifier from a Gaana page:

```
https://gaana.com/song/tyler-herro        → tyler-herro
https://gaana.com/album/tyler-herro       → tyler-herro
https://gaana.com/artist/jack-harlow      → jack-harlow
https://gaana.com/playlist/gaana-dj-...   → gaana-dj-gaana-international-top-50
```

Search results also return `seokey`, `artist_seokeys`, and `album_seokey`.

### Finding an artist ID

Artist IDs are numeric. Get them from search results:

```
GET /songs/search?query=tyler herro
→ [{ "artist_ids": "817522", ... }]
```

### Examples

```sh
curl "http://127.0.0.1:8000/songs/search?query=tyler+herro&limit=5"
curl "http://127.0.0.1:8000/songs/info?seokey=tyler-herro"
curl "http://127.0.0.1:8000/albums/info?seokey=tyler-herro"
curl "http://127.0.0.1:8000/artists/info?seokey=jack-harlow&limit=5&page=1"
curl "http://127.0.0.1:8000/artists/similar?artist_id=817522"
curl "http://127.0.0.1:8000/trending?language=English"
curl "http://127.0.0.1:8000/newreleases?language=English"
curl "http://127.0.0.1:8000/charts"
curl "http://127.0.0.1:8000/playlists/info?seokey=gaana-dj-gaana-international-top-50"
```

### Example response

```json
[
  {
    "seokey": "tyler-herro",
    "title": "Tyler Herro",
    "artists": "Jack Harlow",
    "artist_seokeys": "jack-harlow",
    "artist_ids": "817522",
    "album": "Tyler Herro",
    "album_id": "3487503",
    "duration": "156",
    "language": "English",
    "genres": "Hip Hop",
    "is_explicit": true,
    "images": {
      "urls": {
        "large_artwork": "https://.../size_l.jpg",
        "medium_artwork": "https://.../size_m.jpg",
        "small_artwork": "https://.../size_s.jpg"
      }
    },
    "stream_urls": {
      "urls": {
        "very_high_quality": "https://.../320.mp4.master.m3u8?...",
        "high_quality": "https://.../128.mp4.master.m3u8?...",
        "medium_quality": "https://.../64.mp4.master.m3u8?...",
        "low_quality": "https://.../16.mp4.master.m3u8?..."
      }
    }
  }
]
```

## Local Development

```sh
git clone https://github.com/ZingyTomato/GaanaPy
cd GaanaPy

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 -m uvicorn app:app --reload
```

Open http://127.0.0.1:8000/docs.

### Tests

```sh
pip install pytest pytest-asyncio
python3 -m pytest tests/ -v
```

## Docker

```yaml
services:
  gaanapy:
    image: zingytomato/gaanapy:main
    container_name: gaanapy
    ports:
      - "8000:8000"
    restart: unless-stopped
```

## Contributing

Open an issue for bugs or suggestions.
