import pytest
from unittest.mock import AsyncMock
from api.functions import Functions
from api.errors import Errors
from api.artists.artists import Artists 

class FakeFormatter(Artists):
    def __init__(self):
        self.functions = AsyncMock(spec=Functions)
        self.errors = AsyncMock(spec=Errors)
        self.info = False ## Don't get artist tracks
        

@pytest.mark.asyncio
async def test_format_json_artists():
    formatter = FakeFormatter()

    gaana_input = {
        "artist": [
            {
                "seokey": "artist-seokey-123",
                "artist_id": "artist-id-456",
                "name": "Test Artist",
                "songs": 42,
                "albums": 5,
                "favorite_count": 1000,
                "atw": "https://cdn.gaana.com/images/artist/size_m/artist123.jpg"
            }
        ]
    }

    result = await formatter.format_json_artists(gaana_input)

    assert result["seokey"] == "artist-seokey-123"
    assert result["images"]["urls"]["large_artwork"] == "https://cdn.gaana.com/images/artist/size_l/artist123.jpg"
    assert "artist_id" in result
    assert "artist_url" in result
    assert "top_tracks" not in result ## Didn't request tracks
    
@pytest.mark.asyncio
async def test_format_json_similar_artists():
    formatter = FakeFormatter()

    gaana_input = {
        "seokey": "artist-seokey-789",
        "entity_id": "artist-id-321",
        "name": "Mock Artist",
        "entity_info": [
            {"value": 7},   # album_count
            {"value": 42}   # song_count
        ],
        "favorite_count": 555,
        "atw": "https://cdn.gaana.com/images/artist/size_m/artist789.jpg"
    }

    result = await formatter.format_json_similar_artists(gaana_input)

    assert result["seokey"] == "artist-seokey-789"
    assert result["images"]["urls"]["large_artwork"] == "https://cdn.gaana.com/images/artist/size_l/artist789.jpg"
    assert "artist_id" in result
    assert "artist_url" in result