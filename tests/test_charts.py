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
            {}, {}, {}, {}, {}, {}, {"value": 1},  # index 6 = is_explicit
            {}, {}, {}, {}, {}, {"value": 99999}   # last = play_count
        ],
        "atw": "https://cdn.gaana.com/images/playlist/size_m.jpg"
    }


    result = await formatter.format_json_charts(gaana_input)

    assert result["seokey"] == "test-playlist-123"
    assert result["images"]["urls"]["large_artwork"] == "https://cdn.gaana.com/images/playlist/size_l.jpg"
    assert "playlist_id" in result
    assert "playlist_url" in result