import pytest
from unittest.mock import AsyncMock
from api.functions import Functions
from api.charts.charts import Charts


class FakeFormatter(Charts):
    def __init__(self):
        self.functions = AsyncMock(spec=Functions)


@pytest.mark.asyncio
async def test_format_json_charts():
    formatter = FakeFormatter()

    formatter.functions.isExplicit.return_value = True

    gaana_input = {
        "seokey": "test-playlist-123",
        "entity_id": "playlist-456",
        "name": "Test Playlist",
        "language": "English",
        "favorite_count": 789,
        "entity_info": [
            {}, {}, {}, {}, {}, {}, {"value": 1},
            {}, {}, {}, {}, {}, {"value": 99999}
        ],
        "atw": "https://cdn.gaana.com/images/playlist/size_m.jpg"
    }

    result = await formatter.format_json_charts(gaana_input)

    assert result["seokey"] == "test-playlist-123"
    assert result["images"]["urls"]["large_artwork"] == "https://cdn.gaana.com/images/playlist/size_l.jpg"
    assert "playlist_id" in result
    assert "playlist_url" in result


@pytest.mark.asyncio
async def test_format_json_charts_missing_keys():
    formatter = FakeFormatter()
    formatter.functions.isExplicit.return_value = False

    result = await formatter.format_json_charts({})

    assert result["seokey"] == ""
    assert result["playlist_id"] == ""
    assert result["title"] == ""
    assert result["language"] == ""
    assert result["favorite_count"] == ""
    assert result["is_explicit"] == False
    assert result["play_count"] == ""
    assert result["playlist_url"] == ""
    assert result["images"]["urls"]["large_artwork"] == ""
    assert result["images"]["urls"]["medium_artwork"] == ""
    assert result["images"]["urls"]["small_artwork"] == ""


@pytest.mark.asyncio
async def test_format_json_charts_short_entity_info():
    formatter = FakeFormatter()
    formatter.functions.isExplicit.return_value = False

    result = await formatter.format_json_charts({
        "entity_info": [{"value": "only_one"}]
    })

    assert result["is_explicit"] == False
    assert result["play_count"] == "only_one"


@pytest.mark.asyncio
async def test_format_json_charts_empty_entity_info():
    formatter = FakeFormatter()
    formatter.functions.isExplicit.return_value = False

    result = await formatter.format_json_charts({
        "entity_info": []
    })

    assert result["is_explicit"] == False
    assert result["play_count"] == ""


@pytest.mark.asyncio
async def test_format_json_charts_missing_atw():
    formatter = FakeFormatter()
    formatter.functions.isExplicit.return_value = False

    result = await formatter.format_json_charts({
        "entity_info": [{}, {}, {}, {}, {}, {}, {"value": 1}, {"value": 100}]
    })

    assert result["images"]["urls"]["large_artwork"] == ""
    assert result["images"]["urls"]["medium_artwork"] == ""
    assert result["images"]["urls"]["small_artwork"] == ""
