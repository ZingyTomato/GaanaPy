import pytest
from unittest.mock import AsyncMock
from api.functions import Functions
from api.errors import Errors
from api.albums.albums import Albums 

class FakeFormatter(Albums):
    def __init__(self):
        self.functions = AsyncMock(spec=Functions)
        self.errors = AsyncMock(spec=Errors)
        self.info = False ## Don't get album tracks

@pytest.mark.asyncio
async def test_format_json_albums():
    formatter = FakeFormatter()
    
    formatter.functions.findArtistNames.return_value = "Artist A, Artist B"
    formatter.functions.findArtistSeoKeys.return_value = "artist-a, artist-b"
    formatter.functions.findArtistIds.return_value = "id1, id2"
    formatter.functions.isExplicit.return_value = True

    gaana_input = {
        "album": {
            "seokey": "test-album-seokey",
            "album_id": "album-123",
            "title": "Greatest Hits",
            "artist": [{}],
            "duration": "3600",
            "parental_warning": 1,
            "language": "English",
            "recordlevel": "Test Label",
            "trackcount": 10,
            "release_date": "2020-01-01",
            "al_play_ct": 123456,
            "favorite_count": 7890,
            "artwork": "https://cdn.gaana.com/images/test/size_s.jpg"
        },  
    }


    result = await formatter.format_json_albums(gaana_input)

    assert result["seokey"] == "test-album-seokey"
    assert result["images"]["urls"]["large_artwork"] == "https://cdn.gaana.com/images/test/size_l.jpg"
    assert "album_id" in result
    assert "album_url" in result
    assert "tracks" not in result ## Didn't request tracks