import pytest
from api.functions import Functions

functions = Functions()


@pytest.mark.asyncio
async def test_decryptLink_valid():
    encrypted_link = """6unD0wQzn85Ci6nCVEVdeIA7deSHj0knLx6xEPiF6fFfdCMwZIWVZPbTynyqimz2BOdkjXRitpDzh5jagNiqSN
    JHAmyyCnLS9m2zLLhKLs5Qw5BUTk8AHPWus5HhxmysEmE/KJP+vkXzCY7DC4PIk1+Fz/OfjagcutKzs0WBs3FMixnMvbhRhs6LpEPr1AYH1
    RJW5LRDBdhsoA2sJZNLQZCVzrTiawu1OIL2g9nhJMDW0nSuiy03PRAPp842qB5ooE2vMg2HlMF8Gk0Gl7s1NLWEc3cdxiwAXhAolkV+yYBP
    4KzRUAjLqP4EsUUcB1n2w="""
    decrypted_link = """https://vodhlsgaana-ebw.akamaized.net/hls/83/6437283/47470670/64.mp4.master.m3u8?hdnts=st=1767108041~exp=1767122441~acl=/hls/83/6437283/47470670/*~hmac=6b4f07f96821b88c2509a69ac8d3e70fad19b5a5295b39cf98044dccca31a404"""

    result = await functions.decryptLink(encrypted_link.strip())
    assert result == decrypted_link.strip()


@pytest.mark.asyncio
async def test_decryptLink_empty():
    result = await functions.decryptLink("")
    assert result == ""


@pytest.mark.asyncio
async def test_decryptLink_short():
    result = await functions.decryptLink("abc")
    assert result == ""


@pytest.mark.asyncio
async def test_decryptLink_invalid_base64():
    result = await functions.decryptLink("5xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    assert result == ""


@pytest.mark.asyncio
async def test_findArtistNames_valid():
    artists = [{"name": "Gaana"}, {"name": "Py"}]
    result = await functions.findArtistNames(artists)
    assert result == "Gaana, Py"


@pytest.mark.asyncio
async def test_findArtistNames_empty():
    assert await functions.findArtistNames([]) == ""


@pytest.mark.asyncio
async def test_findArtistNames_missing_key():
    result = await functions.findArtistNames([{"not_name": "x"}])
    assert result == ""


@pytest.mark.asyncio
async def test_findArtistNames_none():
    result = await functions.findArtistNames(None)
    assert result == ""


@pytest.mark.asyncio
async def test_findArtistSeoKeys_valid():
    seokeys = [{"seokey": "Gaana"}, {"seokey": "Py"}]
    result = await functions.findArtistSeoKeys(seokeys)
    assert result == "Gaana, Py"


@pytest.mark.asyncio
async def test_findArtistSeoKeys_empty():
    assert await functions.findArtistSeoKeys([]) == ""


@pytest.mark.asyncio
async def test_findArtistSeoKeys_missing_key():
    result = await functions.findArtistSeoKeys([{"not_seokey": "x"}])
    assert result == ""


@pytest.mark.asyncio
async def test_findArtistIds_valid():
    artist_ids = [{"artist_id": "Gaana"}, {"artist_id": "Py"}]
    result = await functions.findArtistIds(artist_ids)
    assert result == "Gaana, Py"


@pytest.mark.asyncio
async def test_findArtistIds_empty():
    assert await functions.findArtistIds([]) == ""


@pytest.mark.asyncio
async def test_findArtistIds_missing_key():
    result = await functions.findArtistIds([{"not_id": "x"}])
    assert result == ""


@pytest.mark.asyncio
async def test_findGenres_valid():
    genres = [{"name": "Pop"}, {"name": "Rock"}]
    result = await functions.findGenres(genres)
    assert result == "Pop, Rock"


@pytest.mark.asyncio
async def test_findGenres_empty():
    result = await functions.findGenres([])
    assert result == ""


@pytest.mark.asyncio
async def test_findGenres_missing_key():
    result = await functions.findGenres([{"not_name": "x"}])
    assert result == ""


@pytest.mark.asyncio
async def test_isExplicit():
    assert await functions.isExplicit(1) == True
    assert await functions.isExplicit(0) == False


@pytest.mark.asyncio
async def test_isExplicit_non_int():
    assert await functions.isExplicit(None) == False
    assert await functions.isExplicit("1") == False
