import pytest
from unittest.mock import AsyncMock
from api.functions import Functions
from api.errors import Errors
from api.songs.songs import Songs 

class FakeFormatter(Songs):
    def __init__(self):
        self.functions = AsyncMock(spec=Functions)
        self.errors = AsyncMock(spec=Errors)

@pytest.mark.asyncio
async def test_format_json_songs():
    formatter = FakeFormatter()
    
    formatter.functions.findArtistNames.return_value = "Artist A, Artist B"
    formatter.functions.findArtistSeoKeys.return_value = "artist-a, artist-b"
    formatter.functions.findArtistIds.return_value = "id1, id2"
    formatter.functions.findGenres.return_value = "Pop"
    formatter.functions.isExplicit.return_value = True
    formatter.functions.decryptLink.return_value = "https://cdn.gaana.com/song/64.mp4"

    gaana_input = {
        "seokey": "test-song",
        "albumseokey": "test-album",
        "track_id": "123",
        "track_title": "Test Track",
        "artist": [{}],
        "artist_detail": [{"atw": "http://img.test"}],
        "album_title": "Test Album",
        "album_id": "456",
        "duration": "180",
        "popularity": "100",
        "gener": [{}],
        "parental_warning": 1,
        "language": "English",
        "vendor_name": "Test Label",
        "release_date": "2020-01-01",
        "play_ct": 9999,
        "total_favourite_count": 1234,
        "artwork_large": "https://cdn.gaana.com/images/test/size_l.jpg",
        "artwork_web": "https://cdn.gaana.com/images/test/size_m.jpg",
        "artwork": "https://cdn.gaana.com/images/test/size_s.jpg",
        "urls": {
            "medium": {
                "message": "encryptedurl123"
            }
        }
    }

    result = await formatter.format_json_songs(gaana_input)

    assert result["seokey"] == "test-song"
    assert result["stream_urls"]["urls"]["very_high_quality"] == "https://cdn.gaana.com/song/320.mp4"
    assert result["images"]["urls"]["large_artwork"] == "https://cdn.gaana.com/images/test/size_l.jpg"
    assert "track_id" in result
    assert "stream_urls" in result