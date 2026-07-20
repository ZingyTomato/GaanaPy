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


@pytest.mark.asyncio
async def test_format_json_songs_missing_keys():
    formatter = FakeFormatter()
    formatter.functions.findArtistNames.return_value = ""
    formatter.functions.findArtistSeoKeys.return_value = ""
    formatter.functions.findArtistIds.return_value = ""
    formatter.functions.findGenres.return_value = ""
    formatter.functions.isExplicit.return_value = False

    result = await formatter.format_json_songs({"seokey": "minimal"})

    assert result["seokey"] == "minimal"
    assert result["album_seokey"] == ""
    assert result["track_id"] == ""
    assert result["title"] == ""
    assert result["artists"] == ""
    assert result["artist_image"] == ""
    assert result["album"] == ""
    assert result["album_id"] == ""
    assert result["duration"] == ""
    assert result["popularity"] == ""
    assert result["genres"] == ""
    assert result["is_explicit"] == False
    assert result["language"] == ""
    assert result["label"] == ""
    assert result["release_date"] == ""
    assert result["play_count"] == ""
    assert result["favorite_count"] == ""
    assert result["images"]["urls"]["large_artwork"] == ""
    assert result["images"]["urls"]["medium_artwork"] == ""
    assert result["images"]["urls"]["small_artwork"] == ""
    assert result["stream_urls"]["urls"]["very_high_quality"] == ""
    assert result["stream_urls"]["urls"]["high_quality"] == ""
    assert result["stream_urls"]["urls"]["medium_quality"] == ""
    assert result["stream_urls"]["urls"]["low_quality"] == ""


@pytest.mark.asyncio
async def test_format_json_songs_missing_seokey():
    formatter = FakeFormatter()
    formatter.errors.invalid_seokey.return_value = {"error": "Invalid Seokey!"}

    result = await formatter.format_json_songs({})

    assert result == {"error": "Invalid Seokey!"}


@pytest.mark.asyncio
async def test_format_json_songs_no_urls():
    formatter = FakeFormatter()
    formatter.functions.findArtistNames.return_value = "Artist"
    formatter.functions.findArtistSeoKeys.return_value = "artist"
    formatter.functions.findArtistIds.return_value = "1"
    formatter.functions.findGenres.return_value = ""
    formatter.functions.isExplicit.return_value = False

    result = await formatter.format_json_songs({"seokey": "test"})

    assert result["stream_urls"]["urls"]["very_high_quality"] == ""
    assert result["stream_urls"]["urls"]["high_quality"] == ""
    assert result["stream_urls"]["urls"]["medium_quality"] == ""
    assert result["stream_urls"]["urls"]["low_quality"] == ""


@pytest.mark.asyncio
async def test_format_json_songs_decryptLink_fails():
    formatter = FakeFormatter()
    formatter.functions.findArtistNames.return_value = ""
    formatter.functions.findArtistSeoKeys.return_value = ""
    formatter.functions.findArtistIds.return_value = ""
    formatter.functions.findGenres.return_value = ""
    formatter.functions.isExplicit.return_value = False
    formatter.functions.decryptLink.return_value = ""

    gaana_input = {
        "seokey": "test",
        "urls": {"medium": {"message": "bad_encrypted_data"}}
    }

    result = await formatter.format_json_songs(gaana_input)

    assert result["stream_urls"]["urls"]["very_high_quality"] == ""
    assert result["stream_urls"]["urls"]["medium_quality"] == ""
