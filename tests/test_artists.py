import pytest
from unittest.mock import AsyncMock
from api.functions import Functions
from api.errors import Errors
from api.artists.artists import Artists


class FakeFormatter(Artists):
    def __init__(self):
        self.functions = AsyncMock(spec=Functions)
        self.errors = AsyncMock(spec=Errors)


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
    assert "top_tracks" not in result


@pytest.mark.asyncio
async def test_format_json_artists_missing_keys():
    formatter = FakeFormatter()

    result = await formatter.format_json_artists({
        "artist": [{"seokey": "minimal"}]
    })

    assert result["seokey"] == "minimal"
    assert result["artist_id"] == ""
    assert result["name"] == ""
    assert result["song_count"] == ""
    assert result["album_count"] == ""
    assert result["favorite_count"] == ""
    assert result["images"]["urls"]["large_artwork"] == ""
    assert result["images"]["urls"]["medium_artwork"] == ""
    assert result["images"]["urls"]["small_artwork"] == ""
    assert "top_tracks" not in result


@pytest.mark.asyncio
async def test_format_json_artists_no_artist_list():
    formatter = FakeFormatter()
    formatter.errors.invalid_seokey.return_value = {"error": "Invalid Seokey!"}

    result = await formatter.format_json_artists({})

    assert result == {"error": "Invalid Seokey!"}


@pytest.mark.asyncio
async def test_format_json_artists_empty_artist_list():
    formatter = FakeFormatter()
    formatter.errors.invalid_seokey.return_value = {"error": "Invalid Seokey!"}

    result = await formatter.format_json_artists({"artist": []})

    assert result == {"error": "Invalid Seokey!"}


@pytest.mark.asyncio
async def test_format_json_artists_no_seokey():
    formatter = FakeFormatter()
    formatter.errors.invalid_seokey.return_value = {"error": "Invalid Seokey!"}

    result = await formatter.format_json_artists({"artist": [{"name": "No Seokey"}]})

    assert result == {"error": "Invalid Seokey!"}


@pytest.mark.asyncio
async def test_format_json_similar_artists():
    formatter = FakeFormatter()

    gaana_input = {
        "seokey": "artist-seokey-789",
        "entity_id": "artist-id-321",
        "name": "Mock Artist",
        "entity_info": [
            {"value": 7},
            {"value": 42}
        ],
        "favorite_count": 555,
        "atw": "https://cdn.gaana.com/images/artist/size_m/artist789.jpg"
    }

    result = await formatter.format_json_similar_artists(gaana_input)

    assert result["seokey"] == "artist-seokey-789"
    assert result["images"]["urls"]["large_artwork"] == "https://cdn.gaana.com/images/artist/size_l/artist789.jpg"
    assert "artist_id" in result
    assert "artist_url" in result


@pytest.mark.asyncio
async def test_format_json_similar_artists_missing_keys():
    formatter = FakeFormatter()

    result = await formatter.format_json_similar_artists({"seokey": "minimal"})

    assert result["seokey"] == "minimal"
    assert result["artist_id"] == ""
    assert result["name"] == ""
    assert result["song_count"] == ""
    assert result["album_count"] == ""
    assert result["favorite_count"] == ""
    assert result["images"]["urls"]["large_artwork"] == ""
    assert result["images"]["urls"]["medium_artwork"] == ""
    assert result["images"]["urls"]["small_artwork"] == ""


@pytest.mark.asyncio
async def test_format_json_similar_artists_no_seokey():
    formatter = FakeFormatter()
    formatter.errors.invalid_seokey.return_value = {"error": "Invalid Seokey!"}

    result = await formatter.format_json_similar_artists({})

    assert result == {"error": "Invalid Seokey!"}


@pytest.mark.asyncio
async def test_format_json_similar_artists_empty_entity_info():
    formatter = FakeFormatter()

    result = await formatter.format_json_similar_artists({
        "seokey": "test",
        "entity_info": []
    })

    assert result["album_count"] == ""
    assert result["song_count"] == ""
