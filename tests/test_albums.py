import pytest
from unittest.mock import AsyncMock
from api.functions import Functions
from api.errors import Errors
from api.albums.albums import Albums


class FakeFormatter(Albums):
    def __init__(self):
        self.functions = AsyncMock(spec=Functions)
        self.errors = AsyncMock(spec=Errors)


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
    assert "tracks" not in result


@pytest.mark.asyncio
async def test_format_json_albums_missing_keys():
    formatter = FakeFormatter()
    formatter.functions.findArtistNames.return_value = ""
    formatter.functions.findArtistSeoKeys.return_value = ""
    formatter.functions.findArtistIds.return_value = ""
    formatter.functions.isExplicit.return_value = False

    result = await formatter.format_json_albums({"album": {"seokey": "minimal"}})

    assert result["seokey"] == "minimal"
    assert result["album_id"] == ""
    assert result["title"] == ""
    assert result["artists"] == ""
    assert result["artist_seokeys"] == ""
    assert result["artist_ids"] == ""
    assert result["duration"] == ""
    assert result["is_explicit"] == False
    assert result["language"] == ""
    assert result["label"] == ""
    assert result["track_count"] == ""
    assert result["release_date"] == ""
    assert result["play_count"] == ""
    assert result["favorite_count"] == ""
    assert result["images"]["urls"]["large_artwork"] == ""
    assert result["images"]["urls"]["medium_artwork"] == ""
    assert result["images"]["urls"]["small_artwork"] == ""
    assert "tracks" not in result


@pytest.mark.asyncio
async def test_format_json_albums_no_album():
    formatter = FakeFormatter()
    formatter.errors.no_results.return_value = {"error": "Unable to find any results!"}

    result = await formatter.format_json_albums({})

    assert result == {"error": "Unable to find any results!"}


@pytest.mark.asyncio
async def test_format_json_albums_album_no_seokey():
    formatter = FakeFormatter()
    formatter.errors.no_results.return_value = {"error": "Unable to find any results!"}

    result = await formatter.format_json_albums({"album": {"title": "No Seokey"}})

    assert result == {"error": "Unable to find any results!"}


@pytest.mark.asyncio
async def test_format_json_albums_missing_artist_info():
    formatter = FakeFormatter()
    formatter.functions.isExplicit.return_value = False
    formatter.functions.findArtistNames.return_value = ""
    formatter.functions.findArtistSeoKeys.return_value = ""
    formatter.functions.findArtistIds.return_value = ""

    result = await formatter.format_json_albums({
        "album": {
            "seokey": "test",
            "album_id": "123",
            "title": "Test",
            "duration": "100",
            "parental_warning": 0,
            "language": "",
            "recordlevel": "",
            "trackcount": "",
            "al_play_ct": "",
            "favorite_count": "",
            "artwork": ""
        }
    })

    assert result["seokey"] == "test"
    assert result["artists"] == ""
